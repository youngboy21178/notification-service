CREATE_API_KEYS_TABLE = (
    "CREATE TABLE IF NOT EXISTS api_keys ("
    "id INTEGER PRIMARY KEY ,"
    "hashed_api_key TEXT NOT NULL UNIQUE)"
)
CREATE_NOTIFICATION_REPORT_TABLE = (
    "CREATE TABLE IF NOT EXISTS notifications_report ("
    "id INTEGER PRIMARY KEY ,"
    "notification_id TEXT NOT NULL ,"
    "error_message TEXT ,"
    "status TEXT NOT NULL,"
    "created_at TEXT NOT NULL,"
    "sent_at TEXT NOT NULL,"
    
    "encrypted_data TEXT NOT NULL," # user_api | channel | sent_to
    "encryption_iv BLOB NOT NULL,"
    "encryption_tag BLOB NOT NULL)"

)

INSERT_NOTIFICATION_REPORT_TABLE = (
    "INSERT INTO notifications_report ("
    "notification_id, "
    "error_message, "
    "status, "
    "created_at, "
    "sent_at,"
    
    "encrypted_data, "
    "encryption_iv, "
    "encryption_tag) "
    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
)

INSERT_API_KEYS_TABLE = (
    "INSERT INTO api_keys (hashed_api_key) VALUES (?)"
    )

GET_NOTIFICATION_REPORT_TABLE = ("SELECT * FROM notifications_report")
GET_NOTIFICATION_REPORT_TABLE_WITH_ID = ("SELECT * FROM notifications_report WHERE notification_id = ?")
GET_API_KEYS_TABLE = ("SELECT hashed_api_key FROM api_keys;")

UPDATE_NOTIFICATION_STATUS_AND_ERROR = (
    "UPDATE notifications_report "
    "SET status = ?, error_message = ? "
    "WHERE notification_id = ?"
)

