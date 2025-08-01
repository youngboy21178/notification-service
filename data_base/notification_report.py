
import aiosqlite, asyncio, os, random, string, datetime
from fastapi import HTTPException

from utils.hashing import *
from data_base.models import *
from utils.validators import Notification
from utils.encryption import *


DATABASE_URL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "sqlite_data_base.db")



async def _get_connection()->aiosqlite.core.Connection:
    conn = await aiosqlite.connect(DATABASE_URL)
    return conn

async def on_startup():
    db = await _get_connection()
    try:
        await db.execute(CREATE_NOTIFICATION_REPORT_TABLE)
        await db.commit()
    finally:
        await db.close()

async def add_notification(validator_response:dict,
                           service_response:dict,
                           api_key:str,
                           sent_at:str=None) -> str:

    conn = await _get_connection()
    notification_id = await _generate_message_id(session=conn)
    notification_json = {
        "channel": service_response["channel"],
        "user_api": api_key,
        "notification_id": notification_id,#error_massage
        "error_message": service_response["error_message"],#if service_response.get("error_code") is None else ("scheduled" if sent_at is not None else "failed")
        "status": "failed" if service_response.get("error_code") is not None else ("scheduled" if sent_at is not None else "sent"),
        "created_at": await _get_current_iso_time(),
        "sent_at": await _get_current_iso_time() if sent_at is  None else sent_at,
        "sent_to": validator_response["to"],
    }
    notification = Notification(**notification_json)
    await _insert_notification(notification)
    return notification_id


async def up_date_notification_status(notification_id:str ,
                                      service_response:dict)->None:
    conn = await _get_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute(UPDATE_NOTIFICATION_STATUS_AND_ERROR , (service_response["status"],service_response["error_message"],notification_id))
        await conn.commit()
    finally:
        await conn.close()

async def _get_current_iso_time() -> str:

    now = datetime.datetime.now(datetime.UTC)
    return now.strftime("%Y-%m-%dT%H:%M:%S")

async def _insert_notification(notification:Notification)->None:
    db = await _get_connection()
    try:

        data_to_encrypt = {
            "user_api":notification.user_api,
            "channel":notification.channel,
            "sent_to":notification.sent_to,
        }
        plaintext = json.dumps(data_to_encrypt).encode()
        ciphertext, iv, tag = aes_gcm_encrypt(plaintext)

        cursor = await db.cursor()
        await cursor.execute(INSERT_NOTIFICATION_REPORT_TABLE, (
            notification.notification_id,
            notification.error_message,
            notification.status,
            notification.created_at,
            notification.sent_at,

            ciphertext,
            iv,
            tag,
        ))
        await db.commit()

    finally:
        await db.close()


async def _fetch_notifications(db, query, params=None):
    cursor = await db.cursor()
    response = await cursor.execute(query, params or ())
    return await response.fetchall() if params is None else await response.fetchone()


async def _decrypt_and_validate_notification(notification, api_key):
    ciphertext = notification[6]
    iv = notification[7]
    tag = notification[8]
    decrypted_data = aes_gcm_decrypt(ciphertext, iv, tag)

    if decrypted_data["user_api"] != api_key:
        raise HTTPException(status_code=400, detail="Invalid API key")

    return {
        "channel": decrypted_data["channel"],
        "user_api": decrypted_data["user_api"],
        "status": notification[3],
        "created_at": notification[4],
        "sent_at": notification[5],
        "sent_to": decrypted_data["sent_to"],
        "notification_id": notification[1],
        "error_message": notification[2],
    }




async def _generate_message_id(session, length=16, max_attempts=100):
    characters = string.ascii_letters + string.digits

    for _ in range(max_attempts):
        candidate = ''.join(random.choices(characters, k=length))
        if await _is_notification_id_unique(candidate, session):
            return candidate

async def _is_notification_id_unique(candidate:str,
                                     conn:aiosqlite.core.Connection):
    result = True
    try:
        cursor = await conn.cursor()
        response = await cursor.execute(GET_NOTIFICATION_REPORT_TABLE_WITH_ID , (candidate,))
        response = await response.fetchone()
        if response:
            result = False
    finally:
        return result

async def get_notification_with_id(api_key: str, notification_id: str) -> Notification:
    db = await _get_connection()
    try:
        notification = await _fetch_notifications(db, GET_NOTIFICATION_REPORT_TABLE_WITH_ID, (notification_id,))
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        notification_json = await _decrypt_and_validate_notification(notification, api_key)
        return Notification(**notification_json)
    finally:
        await db.close()


async def get_notification_data(api_key: str) -> list[Notification]:
    db = await _get_connection()
    try:
        notifications = await _fetch_notifications(db, GET_NOTIFICATION_REPORT_TABLE)
        result = []

        for notification in notifications:
            try:
                notification_json = await _decrypt_and_validate_notification(notification, api_key)
                result.append(Notification(**notification_json))
            except HTTPException:
                continue

        return result
    finally:
        await db.close()

