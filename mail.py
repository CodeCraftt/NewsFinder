import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Logging setup
log_file = "scraper.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Function to log messages
def log_message(message):
    print(message)
    logging.info(message)

# Email notification function
def send_email(subject, body, to_email):
    from_email = os.getenv("EMAIL_ADDRESS")  # Load from environment variables
    password = os.getenv("EMAIL_PASSWORD")  # Load from environment variables
    smtp_server = os.getenv("SMTP_SERVER")  # Load from environment variables
    smtp_port = int(os.getenv("SMTP_PORT", 587))  # Default to 587 if not set
    
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
            return  # Exit the function after successful send
        except Exception as e:
            log_message(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                log_message("All attempts to send the email failed.")

# Validate email format
def is_valid_email(email):
    return "@" in email and "." in email

# Extract and process headlines
def extract_headlines(num_pages, headlines_per_page):
    # Mock function for the sake of example
    return [f"Headline {i}" for i in range(num_pages * headlines_per_page)]

# Save headlines to multiple formats
def save_to_csv(data):
    log_message("Saving headlines to CSV...")

def save_to_json(data):
    log_message("Saving headlines to JSON...")

def save_to_txt(data):
    log_message("Saving headlines to TXT...")

# Main execution
def main():
    # User-defined parameters
    num_pages = int(input("Enter number of pages to scrape: "))
    headlines_per_page = int(input("Enter number of headlines per page: "))
    recipient_email = input("Enter recipient email: ")
    
    if not is_valid_email(recipient_email):
        log_message("Invalid email address. Exiting.")
        return

    try:
        log_message("Starting web scraping...")
        headlines_data = extract_headlines(num_pages=num_pages, headlines_per_page=headlines_per_page)
        
        if headlines_data:
            save_to_csv(headlines_data)
            save_to_json(headlines_data)
            save_to_txt(headlines_data)
        
        # Generate a preview of the scraped data for the email
        preview = "\n".join(headlines_data[:5]) + ("\n..." if len(headlines_data) > 5 else "")
        send_email(
            subject="Web Scraping Completed Successfully",
            body=f"The web scraping process completed successfully.\n\nPreview of scraped data:\n{preview}",
            to_email=recipient_email
        )
    except Exception as e:
        log_message(f"Error occurred: {e}")
        send_email(
            subject="Web Scraping Error",
            body=f"An error occurred during the web scraping process:\n{e}",
            to_email=recipient_email
        )
    finally:
        log_message("Execution completed.")

if __name__ == "__main__":
    main()
