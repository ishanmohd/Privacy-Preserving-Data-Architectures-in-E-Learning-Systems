from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

KEY_FILE = "secret.key"

# -----------------------------
# Generate key if not exists
# -----------------------------
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

generate_key()
cipher = Fernet(load_key())

# =====================================================
# TEXT ENCRYPTION (for strings / answers / notes)
# =====================================================
def encrypt_data(data: str) -> bytes:
    return cipher.encrypt(data.encode())

def decrypt_data(data: bytes) -> str:
    return cipher.decrypt(data).decode()

# =====================================================
# BYTE ENCRYPTION (for PDFs / files)
# =====================================================
def encrypt_data_bytes(data: bytes) -> bytes:
    return cipher.encrypt(data)

def decrypt_data_bytes(data: bytes) -> bytes:
    return cipher.decrypt(data)
