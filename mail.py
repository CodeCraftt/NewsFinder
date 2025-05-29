import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import json
import csv
import traceback

# Load environment variables
load_dotenv()

# Logging setup
log_file = "scraper.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Directory for saving files
output_dir = "scraped_data"
os.makedirs(output_dir, exist_ok=True)

# Function to log messages
def log_message(message):
    print(message)
    logging.info(message)

# Email notification function
def send_email(subject, body, to_email):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    
    retries = 3
    for attempt in range(retries):
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            
            message = MIMEMultipart()
            message["From"] = from_email
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            server.sendmail(from_email, to_email, message.as_string())
            server.quit()
            log_message(f"Email sent to {to_email}")
            return
        except Exception as e:
            log_message(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                log_message("All attempts to send the email failed.")

def is_valid_email(email):
    return "@" in email and "." in email

# Mock scraping function
def extract_headlines(num_pages, headlines_per_page):
    return [f"Headline {i + 1}" for i in range(num_pages * headlines_per_page)]

def save_to_csv(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"headlines_{timestamp}.csv")
    log_message(f"Saving headlines to {filename}")
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Headline"])
        for line in data:
            writer.writerow([line])

def save_to_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"headlines_{timestamp}.json")
    log_message(f"Saving headlines to {filename}")
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def save_to_txt(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"headlines_{timestamp}.txt")
    log_message(f"Saving headlines to {filename}")
    with open(filename, "w", encoding='utf-8') as f:
        f.write("\n".join(data))

def main():
    num_pages = int(input("Enter number of pages to scrape: "))
    headlines_per_page = int(input("Enter number of headlines per page: "))
    recipient_email = input("Enter recipient email: ")

    if not is_valid_email(recipient_email):
        log_message("Invalid email address. Exiting.")
        return

    start_time = datetime.now()
    log_message(f"Starting web scraping at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        headlines_data = extract_headlines(num_pages=num_pages, headlines_per_page=headlines_per_page)

        if headlines_data:
            save_to_csv(headlines_data)
            save_to_json(headlines_data)
            save_to_txt(headlines_data)

        preview = "\n".join(headlines_data[:5]) + ("\n..." if len(headlines_data) > 5 else "")
        end_time = datetime.now()
        duration = (end_time - start_time).seconds

        send_email(
            subject="✅ Web Scraping Completed Successfully",
            body=(
                f"The web scraping process completed successfully in {duration} seconds.\n"
                f"Total headlines scraped: {len(headlines_data)}\n\n"
                f"Preview of scraped data:\n{preview}"
            ),
            to_email=recipient_email
        )
    except Exception as e:
        error_trace = traceback.format_exc()
        log_message(f"Error occurred:\n{error_trace}")
        send_email(
            subject="❌ Web Scraping Error",
            body=f"An error occurred during the web scraping process:\n\n{error_trace}",
            to_email=recipient_email
        )
    finally:
        log_message("Execution completed.")

if __name__ == "__main__":
    main()
