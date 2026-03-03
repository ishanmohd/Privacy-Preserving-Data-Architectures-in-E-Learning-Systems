import datetime
import secrets
from flask import current_app, jsonify
from flask_mail import Message
from requests import request

from backend.database import get_db
from privacy.encryption import encrypt_data


@auth_bp.route("/forgot-password", methods=["POST"]) # type: ignore
def forgot_password():
    data = request.json
    db = get_db()
    cur = db.cursor(dictionary=True)

    encrypted_email = encrypt_data(data["email"])

    cur.execute(
        "SELECT id FROM users_identity WHERE email=%s",
        (encrypted_email,)
    )
    user = cur.fetchone()

    if not user:
        return jsonify({"message": "If email exists, reset link sent"}), 200

    reset_token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + datetime.timedelta(minutes=15)

    cur.execute(
        "INSERT INTO password_resets (user_id, reset_token, expires_at) VALUES (%s,%s,%s)",
        (user["id"], reset_token, expires)
    )
    db.commit()

    # 🔐 Send email (same mail setup you already have)
    reset_link = f"http://localhost:5500/reset-password.html?token={reset_token}"

    try:
        mail.send(Message( # pyright: ignore[reportUndefinedVariable]
            subject="Password Reset",
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            recipients=[data["email"]],
            body=f"Reset your password: {reset_link}"
        ))
    except:
        pass

    return jsonify({"message": "If email exists, reset link sent"}), 200
