import requests

BASE_URL = "http://127.0.0.1:5000"

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2ODYzMzc5MSwianRpIjoiM2NkYzk3MzYtMjRiZS00YTYxLTgyOGMtMzJmMzU0YjZiZTYxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3Njg2MzM3OTEsImNzcmYiOiIxZThjM2I1Zi1iNmUwLTQzNDUtOTliOS1jZDYyNzgyNzkyMmUiLCJleHAiOjE3Njg2MzQ2OTEsInJvbGUiOiJhZG1pbiJ9.TvxRQnTswYPczRWpS7jDgnbdwACw4TmUT3LTkL7PZfg"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

response = requests.get(f"{BASE_URL}/admin/analytics", headers=headers)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)
