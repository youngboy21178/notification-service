import asyncio
from datetime import datetime
from data_base.notification_report import up_date_notification_status
from services import mail_service , sms_service

async def delayed_email_send(to: str, message: str, when: str, notification_id: str, subject: str=None):
    delay = (datetime.fromisoformat(when) - datetime.utcnow()).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)

    response = await mail_service.send_email(
        receiver=to,
        email_subject=subject,
        email_body=message
    )
    response.update({"status": "sent" if response.get("error_code") is None else "failed"})
    await up_date_notification_status(notification_id, response)

async def delayed_sms_send(to: str, message: str, when: str , notification_id: str):
    delay = (datetime.fromisoformat(when) - datetime.utcnow()).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)

    response = await sms_service.send_sms(
        to_=to ,
        body=message
    )
    response.update({"status": "sent" if response.get("error_code") is None else "failed"})
    await up_date_notification_status(notification_id, response)