# BBC News Headline Scraper

A Python script that scrapes the latest headlines from the BBC News website. The script uses **Selenium** to navigate the website and extract headlines, which are then saved to CSV, JSON, and TXT formats. The script also checks if the links are valid, logs errors, and handles pagination to scrape headlines from multiple pages.

## Features

- Scrapes the latest headlines from the [BBC News](https://www.bbc.com/news) homepage.
- Extracts headline text, article links, and checks if the links are valid.
- Saves scraped headlines in **CSV**, **JSON**, and **TXT** formats.
- Supports pagination for scraping multiple pages of headlines.
- Logs errors and events in a **log file** (`scraping_log.txt`).
- Handles invalid links gracefully and reports their status.

## Requirements

- **Python 3.6+**
- **Selenium**: For browser automation and scraping.
- **Requests**: To check the validity of URLs.
- **ChromeDriver**: Required for Selenium to control the Chrome browser.

### Install Dependencies

To install the required Python libraries, run the following command:

```bash
pip install selenium requests
