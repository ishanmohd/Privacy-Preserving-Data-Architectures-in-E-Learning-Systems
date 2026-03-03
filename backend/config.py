import os


class Config:
    # 🔐 Security
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    # 🗄️ Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Ishan@123")
    DB_NAME = os.getenv("DB_NAME", "elearning_privacy")

    # 📧 Email (CORRECT)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")      # ✅ correct
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")      # ✅ correct
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
