import requests

BASE_URL = "http://127.0.0.1:5000"

# 🔐 STEP 1: LOGIN (use real values)
login_payload = {
    "user_id": 1,              # change if needed
    "password": "password123", # your password
    "otp": "123456"            # current OTP
}

login_res = requests.post(f"{BASE_URL}/auth/login", json=login_payload)

print("LOGIN STATUS:", login_res.status_code)
print("LOGIN RESPONSE:", login_res.json())

token = login_res.json().get("access_token")

# 🧪 STEP 2: TEST STUDENT ROUTE
headers = {
    "Authorization": f"Bearer {token}"
}

student_res = requests.get(f"{BASE_URL}/student/dashboard", headers=headers)

print("\nSTUDENT ROUTE STATUS:", student_res.status_code)
print("STUDENT ROUTE RESPONSE:", student_res.json())
