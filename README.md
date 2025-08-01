
# 📬 Notification Service API

A simple and extensible notification microservice written in Python using FastAPI.  
It allows you to send notifications via email or SMS, manage API keys, and store reports for each request.

---

## 🚀 Features

- Send email and SMS notifications
- AES-GCM encryption for secure message payloads
- Basic API key authentication
- Notification delivery reporting
- Background task processing
- Modular and clean architecture



---

## 📮 API Endpoints

### 🔐 Authentication
All endpoints require a valid `X-API-KEY` header.

---

### 📤 Send Notification

**POST** `/send`

#### Request Body:
`/send/now/email`
```json
{
  "to": "example@example.com",
  "subject": "Hello!",
  "message": "This is a test email."
}
```

Or for SMS:
`/send/now/sms`
```json
{
  "to": "+421911000000",
  "message": "This is a test SMS."
}
```

#### Response:
```json
{
  "message_id": "p0gmpT1xcVc9Ivv4",
  "status": "send"
}
```

---

### 📑 Get Notification Report

**GET** `/notification/{message_id}`

#### Response:
```json
{
    "channel": "email",
    "user_api": "qXUmqtYkSM7lN26MYSKPURJKGXEtmH6F",
    "notification_id": "p0gmpT1xcVc9Ivv4",
    "error_message": null,
    "status": "scheduled",
    "created_at": "2025-08-01T16:34:46",
    "sent_at": "2025-08-01T20:00:00",
    "sent_to": "maksym.melnyk.o.2007@gmail.com"
}

```

---




## ⚙️Sample of usage 
```Python 

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
```
## 📊 Code Stats

Total Python code lines: **717**
