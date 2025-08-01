import string

import bcrypt , asyncio , secrets





async def hash_api_key(api_key: str) -> bytes: #if bcrypt.checkpw(input_password.encode('utf-8'), hashed_password_from_db):
    bytes_api_key = api_key.encode('utf-8')
    salt = await asyncio.to_thread(bcrypt.gensalt)
    hashed_password = await asyncio.to_thread(bcrypt.hashpw, bytes_api_key, salt)
    return hashed_password

async def generate_api_key(length: int = 32) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

async def verify_api_key(api_key: str, hashed: str) -> bool:
    return await asyncio.to_thread(bcrypt.checkpw ,api_key.encode('utf-8'), hashed)
