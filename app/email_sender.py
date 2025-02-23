# import smtplib
# from email.mime.text import MIMEText
# import os

# # Load environment variables
# SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
# SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
# SMTP_USERNAME = os.getenv("SMTP_USERNAME")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
# APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")  # Default to localhost

# def send_confirmation_email(email: str, token: str):
#     """Send email confirmation link with a dynamic base URL"""
#     confirm_url = f"{APP_BASE_URL}/auth/confirm-email?token={token}"
#     message = MIMEText(f"Click the link to confirm your email: {confirm_url}")
#     message["Subject"] = "Confirm Your Email"
#     message["From"] = SMTP_USERNAME
#     message["To"] = email

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#         server.sendmail(SMTP_USERNAME, email, message.as_string())



import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Your Gmail address
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # App Password or Gmail Password

async def send_email(to_email: str, subject: str, body: str):
    """Send an email using Gmail SMTP"""
    msg = EmailMessage()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            start_tls=True
        )
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage:
# await send_email("recipient@example.com", "Test Subject", "This is a test email.")
