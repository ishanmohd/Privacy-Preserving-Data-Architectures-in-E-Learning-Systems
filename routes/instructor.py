import os
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.jwt_utils import role_required
from backend.database import get_db

# 🔐 Encryption imports
from privacy.encryption import encrypt_data_bytes
from privacy.pdf_protect import add_pdf_password

instructor_bp = Blueprint("instructor", __name__)

# 📁 Upload folder (absolute path)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ------------------------------------
# VIEW QUIZZES
# ------------------------------------
@instructor_bp.route("/quizzes", methods=["GET"])
@jwt_required()
@role_required("instructor")
def view_quizzes():

    instructor_id = get_jwt_identity()

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT id, quiz_name, answers, evaluated
        FROM quizzes
        WHERE instructor_id = %s
    """, (instructor_id,))

    quizzes = cur.fetchall()

    import json

    for q in quizzes:

        answers_data = q.get("answers")

        if answers_data:

            try:
                # First parse
                parsed = json.loads(answers_data)

                # If still string → parse again
                if isinstance(parsed, str):
                    parsed = json.loads(parsed)

                q["answers"] = parsed

            except Exception as e:
                print("Answer parse error:", e)
                q["answers"] = {}

        else:
            q["answers"] = {}

    return jsonify(quizzes)



# ------------------------------------
# VIEW DOUBTS
# ------------------------------------
@instructor_bp.route("/doubts", methods=["GET"])
@jwt_required()
@role_required("instructor")
def view_doubts():
    instructor_id = get_jwt_identity()

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT d.id, d.question, d.reply, d.pseudo_id
        FROM doubts d
        JOIN quizzes q ON d.quiz_id = q.id
        WHERE q.instructor_id = %s
        ORDER BY d.id DESC
    """, (instructor_id,))

    return jsonify(cur.fetchall())


# ------------------------------------
# REPLY DOUBT
# ------------------------------------
@instructor_bp.route("/reply", methods=["POST"])
@jwt_required()
@role_required("instructor")
def reply_doubt():
    data = request.get_json(force=True)
    instructor_id = get_jwt_identity()

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE doubts d
        JOIN quizzes q ON d.quiz_id = q.id
        SET d.reply = %s
        WHERE d.id = %s AND q.instructor_id = %s
    """, (data["reply"], data["doubt_id"], instructor_id))

    db.commit()

    return jsonify({"status": "Reply sent"})


# ------------------------------------
# EVALUATE QUIZ
# ------------------------------------
@instructor_bp.route("/evaluate", methods=["POST"])
@jwt_required()
@role_required("instructor")
def evaluate_quiz():
    data = request.get_json(force=True)
    instructor_id = get_jwt_identity()

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE quizzes
        SET score = %s, evaluated = TRUE
        WHERE id = %s AND instructor_id = %s
    """, (
        data["score"],
        data["quiz_id"],
        instructor_id
    ))

    db.commit()
    return jsonify({"status": "Quiz evaluated"})


# ------------------------------------
# VIEW ASSIGNMENTS
# ------------------------------------
@instructor_bp.route("/assignments", methods=["GET"])
@jwt_required()
@role_required("instructor")
def view_assignments():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT id, filename, uploaded_at
        FROM assignments
        ORDER BY uploaded_at DESC
    """)

    return jsonify(cur.fetchall())


# ------------------------------------
# DOWNLOAD ASSIGNMENT
# ------------------------------------
@instructor_bp.route("/download-assignment/<filename>", methods=["GET"])
@jwt_required()
@role_required("instructor")
def download_assignment(filename):

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    return send_file(filepath, as_attachment=True)


# ------------------------------------
# CREATE STUDY POST (PASSWORD PDF)
# ------------------------------------
@instructor_bp.route("/create-post", methods=["POST"])
@jwt_required()
@role_required("instructor")
def create_post():

    data = request.form
    instructor_id = get_jwt_identity()

    title = data.get("title")
    description = data.get("description")
    content = data.get("content")
    video_url = data.get("video_url")

    # 🔐 NEW → Get password from UI
    pdf_password = data.get("pdf_password")

    # Fallback default password
    if not pdf_password:
        pdf_password = "learnacademy123"

    pdf_file = request.files.get("pdf")
    pdf_filename = None

    # -------------------------------
    # HANDLE PDF UPLOAD
    # -------------------------------
    if pdf_file:

        # Read original PDF bytes
        pdf_bytes = pdf_file.read()

        # 🔐 Apply instructor password
        protected_pdf = add_pdf_password(
            pdf_bytes,
            password=pdf_password
        )

        # 🔒 Encrypt protected PDF
        encrypted = encrypt_data_bytes(protected_pdf)

        pdf_filename = f"{instructor_id}_{pdf_file.filename}.enc"

        filepath = os.path.join(UPLOAD_FOLDER, pdf_filename)

        with open(filepath, "wb") as f:
            f.write(encrypted)

    # -------------------------------
    # STORE POST METADATA
    # -------------------------------
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO study_posts
        (instructor_id, title, description, content, video_url, pdf_filename)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        instructor_id,
        title,
        description,
        content,
        video_url,
        pdf_filename
    ))

    db.commit()

    return jsonify({
        "status": "Post created successfully",
        "pdf_password_used": pdf_password  # debug optional
    })

# ------------------------------------
# GRADE ASSIGNMENT
# ------------------------------------
@instructor_bp.route("/grade-assignment", methods=["POST"])
@jwt_required()
@role_required("instructor")
def grade_assignment():

    data = request.get_json(force=True)

    assignment_id = data.get("assignment_id")
    marks = data.get("marks")
    feedback = data.get("feedback")

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE assignments
        SET marks=%s, feedback=%s
        WHERE id=%s
    """, (marks, feedback, assignment_id))

    db.commit()

    return jsonify({"status": "Assignment graded successfully"})
