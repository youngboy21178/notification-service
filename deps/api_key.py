from fastapi import Depends, HTTPException, Security, status, Header
from fastapi.openapi.models import APIKey
from fastapi.security.api_key import APIKeyHeader
from data_base.api_keys import *


API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Header(alias=API_KEY_NAME)) -> str:
    if await is_api_key_available(api_key):  # Просто додаємо await
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )