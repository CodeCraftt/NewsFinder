import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email notifications
def send_email(subject, body, to_email):
    from_email = "your-email@example.com"  # Replace with your email address
    password = "your-email-password"  # Replace with your email password (or use app password for added security)
    smtp_server = "smtp.example.com"  # Replace with your email provider's SMTP server (e.g., 'smtp.gmail.com')
    smtp_port = 587  # Port for TLS
    
    try:
        # Set up the server and log in
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        # Send the email
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        log_message(f"Email sent to {to_email}")
    
    except Exception as e:
        log_message(f"Error sending email: {e}")

# Modify the `main` function to include email notifications
def main():
    # Set up logging
    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:  # Create log file if it doesn't exist
            log.write(f"Log started at {datetime.now()}\n")
    
    # User-defined parameters (pages and headlines per page)
    num_pages = 2  # Adjust the number of pages to scrape
    headlines_per_page = 10  # Number of headlines to extract per page

    try:
        # Extract headlines and save to CSV, JSON, and TXT
        headlines_data = extract_headlines(num_pages=num_pages, headlines_per_page=headlines_per_page)
        
        if headlines_data:
            save_to_csv(headlines_data)
            save_to_json(headlines_data)
            save_to_txt(headlines_data)
        
        # Send success email notification
        send_email(
            subject="Web Scraping Completed Successfully",
            body="The web scraping process has completed successfully. The headlines have been saved.",
            to_email="recipient-email@example.com"  # Replace with recipient's email
        )
    except Exception as e:
        # Send failure email notification in case of error
        send_email(
            subject="Web Scraping Error",
            body=f"An error occurred during the web scraping process: {e}",
            to_email="recipient-email@example.com"  # Replace with recipient's email
        )
        log_message(f"Error occurred: {e}")

    # Graceful shutdown: Always ensure the driver quits after execution
    driver.quit()

if __name__ == "__main__":
    main()
