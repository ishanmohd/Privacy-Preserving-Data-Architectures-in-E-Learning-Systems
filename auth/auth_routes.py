from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import secrets
import pyotp
from flask_mail import Message

from backend.database import get_db
from backend.extensions import mail, bcrypt
from privacy.encryption import encrypt_data
from privacy.pseudonym import generate_pseudo_id

# ✅ DEFINE BLUEPRINT FIRST
auth_bp = Blueprint("auth", __name__)

# ------------------------
# REGISTER (SEND MFA EMAIL)
# ------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    db = get_db()
    cur = db.cursor()

    email = data["email"]
    email_enc = encrypt_data(email)
    password = bcrypt.generate_password_hash(data["password"]).decode()
    role = data.get("role", "student")

    mfa_secret = pyotp.random_base32()

    cur.execute(
        "INSERT INTO users_identity (email, password, role, mfa_secret) VALUES (%s,%s,%s,%s)",
        (email_enc, password, role, mfa_secret)
    )
    user_id = cur.lastrowid

    pseudo_id = generate_pseudo_id()
    cur.execute(
        "INSERT INTO user_mapping (user_id, pseudo_id) VALUES (%s,%s)",
        (user_id, pseudo_id)
    )

    db.commit()

    # 📧 SEND MFA SECRET VIA EMAIL
    msg = Message(
        subject="Action Required: Set Up MFA for Your Account",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email],
        body=f"""
Hello,

Your account has been successfully created.

To complete login setup, configure MFA using the key below.

MFA Secret Key:
{mfa_secret}

Steps:
1. Open Google Authenticator
2. Choose "Enter a setup key"
3. Enter the key above
4. Select Time-based (TOTP)

Do NOT share this key with anyone.

Regards,
E-Learning Security Team
"""
    )

    try:
        mail.send(msg)
    except Exception as e:
        print("EMAIL FAILED (REGISTER):", e)

    return jsonify({
        "message": "Registered successfully. MFA key sent to email.",
        "user_id": user_id
    }), 200


# ------------------------
# FORGOT PASSWORD (SEND RESET LINK)
# ------------------------
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"message": "If email exists, reset link sent"}), 200

    db = get_db()
    cur = db.cursor(dictionary=True)

    email_enc = encrypt_data(email)
    cur.execute("SELECT id FROM users_identity WHERE email=%s", (email_enc,))
    user = cur.fetchone()

    if not user:
        return jsonify({"message": "If email exists, reset link sent"}), 200

    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=15)

    cur.execute(
        "INSERT INTO password_resets (user_id, reset_token, expires_at) VALUES (%s,%s,%s)",
        (user["id"], token, expires)
    )
    db.commit()

    reset_link = f"http://localhost:5500/reset-password.html?token={token}"
    print("RESET LINK:", reset_link)  # debug only

    msg = Message(
        subject="Password Reset Request",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email],
        body=f"""
Hello,

You requested a password reset for your E-Learning account.

Click the link below to reset your password (valid for 15 minutes):

{reset_link}

If you did not request this, please ignore this email.

Regards,
E-Learning Security Team
"""
    )

    try:
        mail.send(msg)
    except Exception as e:
        print("EMAIL FAILED (RESET):", e)

    return jsonify({"message": "If email exists, reset link sent"}), 200
