import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import openpyxl
from urllib.parse import urljoin, urlparse

def fetch_sitemap_urls(base_url):
    print(f"Checking potential sitemap URLs for base URL: {base_url}")
    potential_sitemaps = ["/sitemap.xml", "/wp-sitemap.xml", "/sitemap_index.xml"]
    for sitemap in potential_sitemaps:
        url = urljoin(base_url, sitemap)
        print(f"Trying sitemap URL: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Sitemap found at: {url}")
                return url
        except requests.exceptions.RequestException as e:
            print(f"Error fetching sitemap {url}: {e}")
    print("No sitemap found.")
    return None

def parse_sitemap_recursive(sitemap_url):
    print(f"Parsing sitemap: {sitemap_url}")
    urls = []
    xml_sitemaps = []
    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        for loc in soup.find_all("loc"):
            loc_url = loc.text.strip()
            print(f"Found URL in sitemap: {loc_url}")
            if loc_url.endswith(".xml"):
                print(f"Found child sitemap: {loc_url}")
                child_urls, child_sitemaps = parse_sitemap_recursive(loc_url)
                urls.extend(child_urls)
                xml_sitemaps.extend(child_sitemaps)
            else:
                urls.append(loc_url)
    except Exception as e:
        print(f"Error parsing sitemap {sitemap_url}: {e}")
    return urls, xml_sitemaps

def extract_slug(url):
    path = urlparse(url).path
    parts = path.strip("/").split("/")
    slug = parts[-1] if parts else "(root)"
    print(f"Extracted slug from URL {url}: {slug}")
    return slug

def scrape_url_details(url):
    print(f"Scraping URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        h1 = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
        meta_description = ""
        if soup.find("meta", attrs={"name": "description"}):
            meta_description = soup.find("meta", attrs={"name": "description"}).get("content", "")

        content_length = len(soup.get_text().split())
        slug = extract_slug(url)

        print(f"Scraped details for URL {url}: H1={h1}, Meta Description={meta_description}, Word Count={content_length}")
        return url, slug, h1, meta_description, content_length
    except Exception as e:
        print(f"Error scraping URL {url}: {e}")
        return url, "", "Error", "Error", 0

def export_to_excel(data, xml_sitemaps, output_path):
    print(f"Exporting data to Excel at {output_path}")
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sitemap Data"

    headers = ["URL", "Slug", "H1", "Meta Description", "Content Length"]
    sheet.append(headers)

    for row in data:
        sheet.append(row)

    if xml_sitemaps:
        sitemap_sheet = workbook.create_sheet(title="XML Sitemaps")
        sitemap_sheet.append(["Sitemap URLs"])
        for sitemap in xml_sitemaps:
            sitemap_sheet.append([sitemap])

    workbook.save(output_path)
    print(f"Data successfully exported to {output_path}")

def process_website():
    base_url = entry.get()
    print(f"Processing website: {base_url}")
    if not base_url:
        messagebox.showerror("Error", "Please enter a website URL.")
        return

    if not base_url.startswith("http"):
        base_url = "http://" + base_url

    if base_url.endswith(".xml"):
        sitemap_url = base_url
    else:
        sitemap_url = fetch_sitemap_urls(base_url)

    if not sitemap_url:
        print("Sitemap not found.")
        messagebox.showerror("Error", "No sitemap found.")
        return

    urls, xml_sitemaps = parse_sitemap_recursive(sitemap_url)
    if not urls:
        print("No URLs found in sitemap.")
        messagebox.showerror("Error", "No URLs found in sitemap.")
        return

    data = []
    for url in urls:
        details = scrape_url_details(url)
        data.append(details)

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        export_to_excel(data, xml_sitemaps, file_path)
        messagebox.showinfo("Success", f"Data exported to {file_path}")
        print(f"Data exported successfully to {file_path}")

# GUI Setup
root = tk.Tk()
root.title("Sitemap Scraper Tool")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Enter Website URL:")
label.grid(row=0, column=0, pady=5)

entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=1, pady=5)

process_button = tk.Button(frame, text="Process", command=process_website)
process_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
