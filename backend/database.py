import mysql.connector
from backend.config import Config


def get_db():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        autocommit=True,
        connection_timeout=10
    )

def close_db():
    global _db
    if _db and _db.is_connected():
        _db.close()
        _db = None

