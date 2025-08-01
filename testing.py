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
