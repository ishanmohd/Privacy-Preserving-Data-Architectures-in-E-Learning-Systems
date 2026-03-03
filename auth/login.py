from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import pyotp

from backend.database import get_db
from backend.extensions import bcrypt

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM users_identity WHERE id=%s", (data["user_id"],))
    user = cur.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid password"}), 401

    totp = pyotp.TOTP(user["mfa_secret"])
    if not totp.verify(data["otp"], valid_window=1):
        return jsonify({"error": "Invalid OTP"}), 401

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"role": user["role"]}
    )

    return jsonify({
        "access_token": token,
        "role": user["role"],
        "user_id": user["id"]
    }), 200
