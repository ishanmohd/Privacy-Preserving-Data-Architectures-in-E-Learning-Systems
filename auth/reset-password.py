import datetime
from flask import jsonify
from flask_bcrypt import Bcrypt
from requests import request

from backend.database import get_db
bcrypt = Bcrypt()

@auth_bp.route("/reset-password", methods=["POST"]) # type: ignore
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Invalid request"}), 400

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM password_resets WHERE reset_token=%s AND used=0",
        (token,)
    )
    reset = cur.fetchone()

    if not reset or reset["expires_at"] < datetime.utcnow():
        return jsonify({"error": "Invalid or expired token"}), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode()

    cur.execute(
        "UPDATE users_identity SET password=%s WHERE id=%s",
        (hashed_password, reset["user_id"])
    )

    cur.execute(
        "UPDATE password_resets SET used=1 WHERE id=%s",
        (reset["id"],)
    )

    db.commit()

    return jsonify({"message": "Password reset successful"}), 200
