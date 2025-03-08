import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "angeladeniseflores199@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "rpbm yjls katl wcrt"  # Replace with your generated app password

# Generate OTP
otp = random.randint(100000, 999999)

def send_otp(receiver_email):
    try:
        # Create email message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = receiver_email
        msg["Subject"] = "Your OTP Code"

        # Email body
        body = f"Your One-Time Password (OTP) is: {otp}\nUse this to proceed with your authentication."
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, receiver_email, msg.as_string())
        server.quit()

        print(f"OTP sent successfully to {receiver_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")

# Example Usage
receiver_email = "andersonandy046@gmail.com"  # Replace with the recipient's email
send_otp(receiver_email)
