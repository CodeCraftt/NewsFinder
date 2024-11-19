from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Setup Chrome options to avoid opening a visible browser window
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open CNN website
driver.get("https://www.cnn.com")

# Function to wait for elements to load
def wait_for_element(selector, by=By.CSS_SELECTOR, timeout=10):
    start_time = time.time()
    while True:
        try:
            element = driver.find_element(by, selector)
            return element
        except:
            if time.time() - start_time > timeout:
                raise Exception(f"Timeout while waiting for {selector}")
            time.sleep(0.5)

# Wait for the top stories to load
wait_for_element(".container__headline", By.CSS_SELECTOR)

# Function to extract headlines, links, and publication time
def get_top_headlines():
    headlines_data = []

    # Find all the top headline containers
    headlines_containers = driver.find_elements(By.CSS_SELECTOR, ".container__headline")
    
    for container in headlines_containers:
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
                "published_time": pub_time
            })

        except Exception as e:
            print(f"Error extracting data from a headline: {e}")

    return headlines_data

# Scroll down to load more content if needed (Handle infinite scroll)
def scroll_to_bottom():
    # Scroll 3 times to simulate loading of new content
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

# Wait for the page to load and then scroll to load more content
scroll_to_bottom()

# Get top headlines from CNN
headlines = get_top_headlines()

# Print and save the headlines
print("\nTop Headlines on CNN:")
for idx, data in enumerate(headlines[:10]):  # Show top 10 headlines
    print(f"{idx + 1}. {data['headline']}")
    print(f"   Link: {data['link']}")
    print(f"   Published: {data['published_time']}")
    print("-" * 80)

# Export the data to a CSV file
def export_to_csv(data, filename="headlines.csv"):
    try:
        with open(filename, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["headline", "link", "published_time"])
            writer.writeheader()
            writer.writerows(data)
        print(f"\nData successfully saved to {filename}")
    except Exception as e:
        print(f"Error exporting data to CSV: {e}")

# Call the function to export data
export_to_csv(headlines)

# Close the driver after operation is complete
driver.quit()
