import asyncio, re , os , aiohttp

from email.message import EmailMessage
from aiosmtplib import send
from dotenv import load_dotenv

import config

load_dotenv()


SENDER = config.sender
EMAIL_PWD = config.email_pwd


async def send_email(receiver : str,
                     email_subject : str,
                     email_body : str,
                     _sender: str = SENDER,
                     _email_pwd: str = EMAIL_PWD,
                     ) -> dict :
    message = EmailMessage()
    message['From'] = _sender
    message['To'] = receiver
    message['Subject'] = (email_subject if email_subject else "Notification Service")
    message.set_content(email_body)

    try :
        await send(
            message,
            hostname='smtp.gmail.com',
            port=587,
            start_tls=True,
            username=_sender,
            password=_email_pwd
        )
        return {
            "channel":"email",
            "error_code": None,
            "error_message": None,
        }
    except Exception as e :
        return {
            "channel": "email",
            "error_code":400,
            "error_message": str(e)
        }

