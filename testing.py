# import base64
#
# import aiohttp
# import asyncio , os
# from utils.encryption import *
#
#
# from utils.validators import *
#
# from data_base.notification_report import *
# #maksym.melnyk.o.2007@gmail.com
# #+421952260910
#
# async def send_message():
#
#     url = "http://127.0.0.1:8000/get-notification-info"
#     headers = {"X-API-Key": "qXUmqtYkSM7lN26MYSKPURJKGXEtmH6F"}
#     payload = {
#         "to": "maksym.melnyk.o.2007@gmail.com",
#         "message": "Привіт! Це повідомлення через aiohttp.",
#         "when":"2025-08-01T20:00:00"
#
#     }
#
#     try:
#         async with aiohttp.ClientSession() as session:
#             print("getting response")
#             async with session.post(url, json=payload, headers=headers) as response:
#                 print("printing response")
#                 if response.status != 200:
#                     print(f"[ERROR] {response.status}")
#                     text = await response.text()
#                     print(f"[ERROR TEXT] {text}")
#                     return
#                 data = await response.json()
#                 print("[STATUS] ", response.status)
#                 print("[RESPONSE]", data)
#     except Exception as e:
#         print(f"[ERR] {e}")
#
# asyncio.run(send_message())
import requests

url = "http://127.0.0.1:8000/send/later/email"
headers = {"X-API-Key": "qXUmqtYkSM7lN26MYSKPURJKGXEtmH6F"}
payload = {
    "to": "exemple@gmail.com",
    "message": "Hello world",
    "message_subject":"Test", #Optional . Basic value is "Notification Service"
    "when":"2025-08-02T20:00:00" #The date must be in the future
}
response = requests.post(url, json=payload, headers=headers)
data = response.json()
print(data)