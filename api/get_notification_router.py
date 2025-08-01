# routers/payments.py
import asyncio

from fastapi import APIRouter, HTTPException , Depends
from pydantic import BaseModel
from typing import Optional
from utils.validators import *
from services import mail_service, sms_service
from background import tasks

from deps.api_key import get_api_key
from data_base.notification_report import *

router = APIRouter(
    prefix="/get-notification-info",
    tags=["get-notification-info"]
)

class NotificationInfo(BaseModel):
    notification_id: str

@router.get("")
async def send_email_later(data: NotificationInfo , api_key = Depends(get_api_key)):
    notification_id = data.notification_id
    if len(notification_id) != 16:
        raise HTTPException(status_code=404, detail="Invalid notification ID")

    response = await get_notification_with_id(api_key, notification_id)
    return response.model_dump()