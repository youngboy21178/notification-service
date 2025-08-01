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
    prefix="/send",
    tags=["send"]
)

class MessageRequest(BaseModel):
    to: str
    message: str


    when : Optional[str] = None
    message_subject: Optional[str] = None


@router.post("/later/email")
async def send_email_later(data: MessageRequest , api_key = Depends(get_api_key)):
    validator_response = await validate_and_extract(data.model_dump() , "email")
    if not validator_response["when"]:
        raise HTTPException(status_code=400, detail="Missing \'when\' parameter for de layed email")
    service_response = {
            "channel": "email",
            "error_code" : None,
            "error_message" : None,
        }
    notification_id = await add_notification(validator_response , service_response , api_key , validator_response["when"] )
    asyncio.create_task(tasks.delayed_email_send(to=validator_response["to"],
                                                       message=validator_response["message"],
                                                       when=validator_response["when"],
                                                       notification_id=notification_id))

    return {"status": "scheduled" ,
            "detail": f"will be delivered {validator_response["when"]}"}


@router.post("/later/sms")
async def send_sms_later(data: MessageRequest, api_key=Depends(get_api_key)):
    validator_response = await validate_and_extract(data.model_dump(), "email")
    if not validator_response["when"]:
        raise HTTPException(status_code=400, detail="Missing \'when\' parameter for delayed email")
    service_response = {
        "channel": "sms",
        "error_code": None,
        "error_message": None,
    }
    notification_id = await add_notification(validator_response, service_response, api_key, validator_response["when"])
    asyncio.create_task(tasks.delayed_sms_send(to=validator_response["to"],
                                                       message=validator_response["message"],
                                                       when=validator_response["when"],
                                                       notification_id=notification_id))

    return {"status": "scheduled",
            "detail": f"will be delivered {validator_response["when"]}"}


@router.post("/now/email")
async def send_email( data: MessageRequest, api_key: str = Depends(get_api_key)):

    validator_response = await validate_and_extract(data.model_dump() , "email")

    email_service_response = await mail_service.send_email(receiver=validator_response["to"] ,
                                              email_subject=validator_response["message_subject"] ,
                                              email_body=validator_response["message"] ,)

    notification_id = await add_notification(validator_response, email_service_response, api_key)

    if email_service_response.get("error_code"):
        raise HTTPException(status_code=500 ,detail=email_service_response["error_massage"]+ f" notification_id = {notification_id}")
    return {"status": "sent",
            "notification_id" : notification_id}

@router.post("/now/sms")
async def send_sms(data: MessageRequest, api_key: str = Depends(get_api_key)):
    validator_response = await validate_and_extract(data.model_dump() , "sms")
    sms_service_response = await sms_service.send_sms(to_=validator_response["to"] ,
                                                      body=validator_response["message"] ,)

    notification_id = await add_notification(validator_response, sms_service_response, api_key)
    if sms_service_response.get("error_code"):
        raise HTTPException(status_code=sms_service_response["error_code"], detail=str(sms_service_response["error_message"])+ f" notification_id = {notification_id}")
    return {"status": "sent",
            "notification_id" : notification_id}
