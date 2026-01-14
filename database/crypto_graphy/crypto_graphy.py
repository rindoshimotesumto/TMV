import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

KEY = os.getenv("DB_SECRET_KEY")

if not KEY:
    raise RuntimeError("DB_SECRET_KEY not set")

f = Fernet(KEY.encode() if isinstance(KEY, str) else KEY)

def encrypted(data: str) -> bytes:
    return f.encrypt(data.encode())

def decrypted(data: bytes) -> str:
    return f.decrypt(data).decode()