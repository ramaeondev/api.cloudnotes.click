import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load your Brevo API key and email details from environment variables
API_KEY = os.getenv("BREVO_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "no-reply@cloudnotes.click")
FROM_NAME = os.getenv("FROM_NAME", "Cloudnotes Notifications")

# Brevo API endpoint for sending transactional emails
API_URL = "https://api.brevo.com/v3/smtp/email"

# Function to send an email using Brevo's API
def send_email(to_email: str, subject: str, body: str):
    """Send an email using Brevo's API"""
    
    # Prepare the payload for the email
    payload = {
        "sender": {
            "email": FROM_EMAIL,
            "name": FROM_NAME
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": body
    }
    
    # Set headers including the API key for authorization
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        # Make the API request to send the email
        response = requests.post(API_URL, json=payload, headers=headers)

        # Check the response from the API
        if response.status_code == 200:
            print(f"Email sent to {to_email}")
        else:
            print(f"Failed to send email: {response.text}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

