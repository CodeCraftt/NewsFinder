from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import json
import logging
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
logging.info("Initializing WebDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open CNN website
logging.info("Opening CNN website...")
driver.get("https://www.cnn.com")

# Function to wait for elements to load
def wait_for_element(selector, by=By.CSS_SELECTOR, timeout=10):
    logging.info(f"Waiting for element: {selector}")
    start_time = time.time()
    while True:
        try:
            element = driver.find_element(by, selector)
            return element
        except Exception:
            if time.time() - start_time > timeout:
                logging.error(f"Timeout while waiting for {selector}")
                raise
            time.sleep(0.5)

# Wait for the top stories to load
wait_for_element(".container__headline", By.CSS_SELECTOR)

# Function to extract headlines, links, and publication time
def get_top_headlines():
    logging.info("Extracting top headlines...")
    headlines_data = []
    retries = 3

    # Find all the top headline containers
    headlines_containers = driver.find_elements(By.CSS_SELECTOR, ".container__headline")
    for container in headlines_containers:
        for attempt in range(retries):
            try:
                # Extract headline text and link
                headline = container.find_element(By.TAG_NAME, "a").text
                link = container.find_element(By.TAG_NAME, "a").get_attribute("href")

                # Optional: Extract publication time (if available)
                try:
                    pub_time = container.find_element(By.CSS_SELECTOR, "span.timestamp").text
                except:
                    pub_time = "Unknown"

                headlines_data.append({
                    "headline": headline,
                    "link": link,
                    "published_time": pub_time,
                })
                break
            except Exception as e:
                if attempt < retries - 1:
                    logging.warning(f"Retrying extraction ({attempt + 1}/{retries})...")
                    time.sleep(1)
                else:
                    logging.error(f"Failed to extract data from a headline: {e}")

    return headlines_data

# Scroll down dynamically to load more content
def scroll_to_bottom():
    logging.info("Scrolling to load more content...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 3

    for _ in range(scroll_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll and extract headlines
scroll_to_bottom()
headlines = get_top_headlines()

# Print and save the headlines
logging.info("\nTop Headlines on CNN:")
for idx, data in enumerate(headlines[:10]):  # Show top 10 headlines
    print(f"{idx + 1}. {data['headline']}")
    print(f"   Link: {data['link']}")
    print(f"   Published: {data['published_time']}")
    print("-" * 80)

# Dynamic filename based on the current date
def get_filename(base_name, ext):
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"{base_name}_{current_date}.{ext}"

# Export data to CSV with dynamic filename
def export_to_csv(data, filename="headlines.csv"):
    filename = get_filename(filename, "csv")
    logging.info(f"Exporting data to {filename}...")
    try:
        with open(filename, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["headline", "link", "published_time"])
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Error exporting data to CSV: {e}")

# Export data to JSON with dynamic filename
def export_to_json(data, filename="headlines.json"):
    filename = get_filename(filename, "json")
    logging.info(f"Exporting data to {filename}...")
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Error exporting data to JSON: {e}")

# Function to filter headlines by keyword
def filter_headlines_by_keyword(headlines, keyword):
    logging.info(f"Filtering headlines by keyword: {keyword}")
    filtered_headlines = [data for data in headlines if keyword.lower() in data["headline"].lower()]
    logging.info(f"Found {len(filtered_headlines)} headlines containing '{keyword}'")
    return filtered_headlines

# Example: Filtering headlines containing the keyword "election"
filtered_headlines = filter_headlines_by_keyword(headlines, "election")

# Export filtered headlines to CSV and JSON
export_to_csv(filtered_headlines)
export_to_json(filtered_headlines)

# Close the driver after operation is complete
logging.info("Closing the WebDriver...")
driver.quit()
