# Sitemap Scraper Tool

The **Sitemap Scraper Tool** is a Python-based utility with a user-friendly GUI for extracting and analyzing URLs from a website's sitemap. It also scrapes details such as H1 tags, meta descriptions, and content length from each URL. The scraped data is exported to an Excel file for easy access and further analysis.

---

## Features
- Automatically detects common sitemap URLs (e.g., `/sitemap.xml`, `/wp-sitemap.xml`).
- Recursively parses XML sitemaps to extract all URLs.
- Scrapes details for each URL, including:
  - Slug
  - H1 tag
  - Meta description
  - Content length (word count).
- Exports data to an Excel file with additional details about XML sitemaps found.

---

## Requirements

### Dependencies
The following Python libraries are required:

- `tkinter`: Built-in GUI library for creating the user interface.
- `requests`: For making HTTP requests to fetch sitemaps and page content.
- `beautifulsoup4`: For parsing HTML/XML content.
- `openpyxl`: For exporting data to Excel files.

### Installation
To install the required dependencies, run the following command:

```bash
pip install requests beautifulsoup4 openpyxl
```

---

## How to Use

### Running the Tool
1. Ensure all dependencies are installed.
2. Save the script as `sitemap_scraper.py`.
3. Run the script using Python:

   ```bash
   python sitemap_scraper.py
   ```

### Using the GUI
1. Enter the base URL of the website in the input field (e.g., `https://example.com`).
2. Click the **Process** button.
3. The tool will detect the sitemap, extract URLs, scrape details, and prompt you to save the output as an Excel file.
4. The exported Excel file will contain:
   - A sheet with the scraped data.
   - A sheet with any additional XML sitemaps discovered during the parsing.

---

## Example

### Input
- Website URL: `https://example.com`

### Output
An Excel file containing:

| URL                          | Slug            | H1          | Meta Description   | Content Length |
|------------------------------|-----------------|-------------|--------------------|----------------|
| https://example.com/page1    | page1           | Welcome     | Page description   | 350            |
| https://example.com/blog     | blog            | Blog Title  | Blog description   | 500            |

---

## Troubleshooting

### Common Errors

- **No sitemap found**: Ensure the website has a valid XML sitemap. If you know the exact sitemap URL, enter it directly in the input field.
- **Timeout or Connection Error**: Check your internet connection or verify the website is accessible.

### Logging
- The tool provides real-time logs in the console to help track progress and debug issues.

---

## License
This tool is open-source and distributed under the MIT License.

---

## Contribution
Feel free to contribute by reporting issues, suggesting features, or submitting pull requests.

---

## Contact
For inquiries or support, contact the developer at onnorokomofficial [at]gmail.com
