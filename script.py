from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import csv
import json
import os
import requests

# Set up the driver with manual chromedriver path (provide the correct path)
service = Service('/path/to/chromedriver')  # Ensure to provide the correct path to chromedriver
driver = webdriver.Chrome(service=service)

# Log file to capture errors and events
log_file = "scraping_log.txt"

# Function to log messages to both the console and a log file
def log_message(message):
    print(message)
    with open(log_file, 'a') as log:
        log.write(f"{datetime.now()} - {message}\n")

# Function to check if the link is valid (returns True if the URL is accessible)
def is_valid_link(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def extract_headlines(num_pages=1, headlines_per_page=10):
    headlines_data = []
    for page in range(num_pages):
        try:
            # Navigate to the news website
            driver.get("https://www.bbc.com/news")
            
            # Wait until the headlines are present (using explicit wait instead of sleep)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
            
            # Find headline elements
            headlines = driver.find_elements(By.CSS_SELECTOR, "h3")

            # Extract the headlines and additional info (e.g., links, publication time)
            for i, headline in enumerate(headlines[:headlines_per_page], start=1):
                text = headline.text
                link = headline.find_element(By.XPATH, './a').get_attribute('href') if headline.find_element(By.XPATH, './a') else 'No link available'
                publish_time = "N/A"  # Placeholder for publish time (could be added if available)
                
                # Check if the link is valid
                link_status = "Valid" if is_valid_link(link) else "Invalid"

                headlines_data.append({
                    'rank': i + page * headlines_per_page,  # Adjust the rank to account for multiple pages
                    'headline': text,
                    'link': link,
                    'publish_time': publish_time,
                    'link_status': link_status
                })

                # Print headlines to console
                log_message(f"{i + page * headlines_per_page}. {text} ({link})")

            # Handle pagination: Move to the next page if a "next" button is found
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a.pagination__next")
                next_button.click()
                WebDriverWait(driver, 10).until(EC.staleness_of(headlines[0]))  # Wait for the page to load
            except Exception as e:
                log_message(f"Could not find 'Next' button or reached the last page: {e}")
                break

        except Exception as e:
            log_message(f"Error occurred while extracting headlines: {e}")
            break

    return headlines_data

def save_to_csv(data, filename="headlines.csv"):
    try:
        # Save data to CSV file
        with open(filename, "w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["rank", "headline", "link", "publish_time", "link_status"])
            writer.writeheader()
            writer.writerows(data)
        log_message(f"Headlines saved to '{filename}'")

    except Exception as e:
        log_message(f"Error saving to CSV: {e}")

def save_to_json(data, filename="headlines.json"):
    try:
        # Save data to JSON file
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        log_message(f"Headlines saved to '{filename}'")

    except Exception as e:
        log_message(f"Error saving to JSON: {e}")

def save_to_txt(data, filename="headlines.txt"):
    try:
        # Save headlines to a plain text file
        with open(filename, "w", encoding="utf-8") as file:
            for item in data:
                file.write(f"Rank: {item['rank']}\nHeadline: {item['headline']}\nLink: {item['link']}\nLink Status: {item['link_status']}\nPublish Time: {item['publish_time']}\n\n")
        log_message(f"Headlines saved to '{filename}'")

    except Exception as e:
        log_message(f"Error saving to TXT: {e}")

def main():
    # Set up logging
    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:  # Create log file if it doesn't exist
            log.write(f"Log started at {datetime.now()}\n")
    
    # User-defined parameters (pages and headlines per page)
    num_pages = 2  # Adjust the number of pages to scrape
    headlines_per_page = 10  # Number of headlines to extract per page

    # Extract headlines and save to CSV, JSON, and TXT
    headlines_data = extract_headlines(num_pages=num_pages, headlines_per_page=headlines_per_page)
    
    if headlines_data:
        save_to_csv(headlines_data)
        save_to_json(headlines_data)
        save_to_txt(headlines_data)

    # Graceful shutdown: Always ensure the driver quits after execution
    driver.quit()

if __name__ == "__main__":
    main()
 