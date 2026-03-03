from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.database import get_db
from privacy.encryption import decrypt_data, decrypt_data_bytes, encrypt_data
import json
import os

student_bp = Blueprint("student", __name__)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------
# Upload Assignment
# ---------------------------
@student_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_assignment():

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    user_id = int(get_jwt_identity())

    db = get_db()
    cur = db.cursor(dictionary=True)

    # Get pseudo_id
    cur.execute(
        "SELECT pseudo_id FROM user_mapping WHERE user_id = %s",
        (user_id,)
    )
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "User mapping not found"}), 400

    pseudo_id = row["pseudo_id"]

    # 🔒 Encrypt bytes (FIXED)
    from privacy.encryption import encrypt_data_bytes

    file_bytes = file.read()
    encrypted_content = encrypt_data_bytes(file_bytes)

    filename = f"{pseudo_id}_{file.filename}.enc"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(encrypted_content)

    # Store metadata
    cur2 = db.cursor()
    cur2.execute(
        "INSERT INTO assignments (pseudo_id, filename) VALUES (%s, %s)",
        (pseudo_id, filename)
    )

    db.commit()

    return jsonify({"status": "uploaded"}), 200


# ---------------------------
# Submit Quiz
# ---------------------------
@student_bp.route("/submit-quiz", methods=["POST"])
@jwt_required()
def submit_quiz():
    data = request.get_json(force=True)
    user_id = int(get_jwt_identity())

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT pseudo_id FROM user_mapping WHERE user_id=%s",
        (user_id,)
    )
    pseudo_id = cur.fetchone()["pseudo_id"]

    cur.execute(
        """
        INSERT INTO quizzes (pseudo_id, quiz_name, answers, instructor_id)
        VALUES (%s,%s,%s,%s)
        """,
        (
            pseudo_id,
            data["quiz_name"],
            json.dumps(data["answers"]),
            data["instructor_id"]
        )
    )

    db.commit()
    return jsonify({"status": "quiz submitted"}), 200

# ---------------------------
# Submit Doubt
# ---------------------------
@student_bp.route("/submit-doubt", methods=["POST"])
@jwt_required()
def submit_doubt():
    data = request.get_json(force=True)
    user_id = int(get_jwt_identity())

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT pseudo_id FROM user_mapping WHERE user_id=%s",
        (user_id,)
    )
    pseudo_id = cur.fetchone()["pseudo_id"]

    cur.execute(
        """
        INSERT INTO doubts (pseudo_id, question, quiz_id)
        VALUES (%s,%s,%s)
        """,
        (
            pseudo_id,
            data["question"],
            data["quiz_id"]
        )
    )

    db.commit()
    return jsonify({"status": "doubt submitted"}), 200

# ---------------------------
# View My Doubts
# ---------------------------
@student_bp.route("/my-doubts", methods=["GET"])
@jwt_required()
def view_my_doubts():
    user_id = int(get_jwt_identity())

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT pseudo_id FROM user_mapping WHERE user_id=%s",
        (user_id,)
    )
    pseudo_id = cur.fetchone()["pseudo_id"]

    cur.execute("""
        SELECT question, reply
        FROM doubts
        WHERE pseudo_id = %s
        ORDER BY id DESC
    """, (pseudo_id,))

    return jsonify(cur.fetchall())

# ---------------------------
# View Scores
# ---------------------------
@student_bp.route("/scores", methods=["GET"])
@jwt_required()
def view_scores():
    user_id = int(get_jwt_identity())

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT pseudo_id FROM user_mapping WHERE user_id=%s",
        (user_id,)
    )
    row = cur.fetchone()
    if not row:
        return jsonify([])

    pseudo_id = row["pseudo_id"]

    cur.execute("""
        SELECT quiz_name, score
        FROM quizzes
        WHERE pseudo_id = %s AND evaluated = TRUE
    """, (pseudo_id,))

    return jsonify(cur.fetchall())

@student_bp.route("/posts", methods=["GET"])
@jwt_required()
def view_posts():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT title, description, content, video_url, pdf_filename, created_at
        FROM study_posts
        ORDER BY created_at DESC
    """)

    return jsonify(cur.fetchall())

@student_bp.route("/assignment-grades", methods=["GET"])
@jwt_required()
def view_assignment_grades():
    user_id = int(get_jwt_identity())

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT pseudo_id FROM user_mapping WHERE user_id=%s",
        (user_id,)
    )
    pseudo_id = cur.fetchone()["pseudo_id"]

    cur.execute("""
        SELECT filename, marks, feedback
        FROM assignments
        WHERE pseudo_id = %s
    """, (pseudo_id,))

    return jsonify(cur.fetchall())

from flask import send_file
import io

@student_bp.route("/download-post-pdf/<filename>", methods=["GET"])
@jwt_required()
def download_post_pdf(filename):

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    # 🔐 Read encrypted file
    with open(filepath, "rb") as f:
        encrypted = f.read()

    # 🔓 Decrypt bytes
    from privacy.encryption import decrypt_data_bytes
    decrypted = decrypt_data_bytes(encrypted)

    # 📄 Send decrypted PDF properly
    return send_file(
        io.BytesIO(decrypted),
        as_attachment=True,
        download_name=filename.replace(".enc", ""),
        mimetype="application/pdf"
    )



