import re

from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator
from typing import Optional , ClassVar
from fastapi import HTTPException
from datetime import datetime
from enum import Enum

from fastapi import HTTPException


class TextTypes(str, Enum):
    SMS = "sms"
    EMAIL = "email"

class Notification(BaseModel):
    channel: str
    user_api: str
    notification_id: Optional[str] = "00000000"
    error_message: Optional[str] = None
    status: str
    created_at: str
    sent_at: str
    sent_to: str



class DataValidator(BaseModel):
    MAX_SMS: ClassVar[int] = 67
    MAX_EMAIL: ClassVar[int] = 10000
    MAX_EMAIL_SUBJECT: ClassVar[int] = 120

    message_type: TextTypes
    message_subject: Optional[str] = None
    when: Optional[str] = None
    message: str
    to: str



    @field_validator('message')
    def validate_message(cls, value: str, info: ValidationInfo) -> str:
        message_type = info.data.get('message_type')

        if message_type is None:
            raise ValueError("text_type is required")

        max_length = {
            TextTypes.SMS: cls.MAX_SMS,
            TextTypes.EMAIL: cls.MAX_EMAIL,

        }[message_type]

        if len(value) > max_length:
            raise ValueError(f"Text exceeds maximum length of {max_length} characters")
        return value



    @field_validator('to')
    def validate_to(cls, value: str, info: ValidationInfo) -> str:
        message_type = info.data.get('message_type')
        if message_type is None:
            raise ValueError("text_type is required")
        match message_type:
            case TextTypes.EMAIL:
                if value and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
                    raise ValueError("Invalid email format")
            case TextTypes.SMS:
                if value and not re.match(r'^\+?[0-9]{10,13}$', value):
                    raise ValueError("Invalid phone number format")
        return value

    @field_validator('when')
    def validate_when(cls, value: str, info: ValidationInfo) :
        if value is None:
            return None
        try:

            parsed = datetime.fromisoformat(value)
            if parsed <= datetime.utcnow():
                raise ValueError("Time must be in the future")
            return value
        except ValueError:
            raise ValueError("Invalid datetime format. Use ISO format, e.g. '2025-07-31T20:00:00'")


async def validate_data(user_data: dict):
    try:
        data_validator = DataValidator(**user_data)
        data = data_validator.model_dump()
        data.update({"status": "success"})
        return data
    except ValidationError as ve:
        return {
            "status": "error",
            "code": 422,
            "errors": ve.errors()
        }
    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "errors": [{"msg": str(e)}]
        }


async def validate_and_extract(data: dict, type_: str):
    data.update({"message_type" : type_})
    response = await validate_data(data)
    if response["status"] == "error":
        raise HTTPException(
            status_code=400,
            detail=str(response["errors"][0]["ctx"]["error"])
        )
    return response