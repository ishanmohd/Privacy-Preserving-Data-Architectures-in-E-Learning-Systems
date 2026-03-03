import requests

BASE = "http://127.0.0.1:5000"
TOKEN = "PASTE_JWT_TOKEN_HERE"

files = {
    "file": open("sample.txt", "rb")
}

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

res = requests.post(f"{BASE}/student/upload", files=files, headers=headers)
print(res.json())
