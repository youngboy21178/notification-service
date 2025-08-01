import os , aiohttp , asyncio , config

from aiohttp.abc import HTTPException
from dotenv import load_dotenv


load_dotenv()
twilio_account_sid = config.twilio_account_sid
twilio_auth_token = config.twilio_auth_token
twilio_number = config.twilio_number




async def send_sms(to_: str ,
                   body: str,
                   from_: str = twilio_number
                   ) -> dict:
    auth = aiohttp.BasicAuth(login=twilio_account_sid, password=twilio_auth_token)
    async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(login=twilio_account_sid, password=twilio_auth_token)) as session:
        response = await session.post(f'https://api.twilio.com/2010-04-01/Accounts/{twilio_account_sid}/Messages.json',
                                  data={'From': from_, 'To': to_, 'Body': body})
        response_json = await response.json()
        check_url = "https://api.twilio.com"+response_json['uri']

        is_sent = False
        time_out = 30
        while not is_sent :
            async with session.get(check_url) as resp:
                data = await resp.json()
                status = data['status']
                if status == "failed" :
                    raise HTTPException(status_code=400,detail="Sending was failed")
                is_sent = (status == "sent")
            await asyncio.sleep(0.5)
            time_out -= 0.5
            if time_out < 0 :
                raise   HTTPException(status_code=400,detail="Sending was failed (timeout)")
        return  {
            "channel": "sms",
            "error_code" : response_json['error_code'],
            "error_message" : response_json['error_message'],
        }
