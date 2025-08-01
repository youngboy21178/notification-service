

import aiosqlite , asyncio , os


from utils.hashing import *
from data_base.models import *


DATABASE_URL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "sqlite_data_base.db")



async def get_connection():
    conn = await aiosqlite.connect(DATABASE_URL)
    #conn.row_factory = aiosqlite.Row
    return conn

async def on_startup():
    db = await get_connection()
    try:
        await db.execute(CREATE_API_KEYS_TABLE)
        await db.commit()
    finally:
        await db.close()

async def create_api_key():
    db = await get_connection()
    try:
        api_key = await generate_api_key()
        print(api_key)
        hashed_api_key = await hash_api_key(api_key)
        cursor = await db.cursor()
        await cursor.execute(INSERT_API_KEYS_TABLE,(hashed_api_key,))
        await db.commit()

    finally:
        await db.close()

async def is_api_key_available(api_key):
    db = await get_connection()
    result = False
    try :

        cursor = await db.cursor()
        result = await cursor.execute(GET_API_KEYS_TABLE)
        # print((await result.fetchall())[0][0])
        for one in (await result.fetchall()):
            hashed_api_key = one[0]
            result = await verify_api_key(api_key, hashed_api_key)
            if result:
                break

    finally:
        await db.close()
        return result




