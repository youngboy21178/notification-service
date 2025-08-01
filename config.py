import os

from dotenv import load_dotenv
load_dotenv()

encryption_key = os.getenv("ENCRYPTION_KEY")

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")

sender = os.getenv("SENDER")
email_pwd = os.getenv("EMAIL_PWD")