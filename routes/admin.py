from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from auth.jwt_utils import role_required
from backend.database import get_db
from privacy.encryption import decrypt_data
import os
import random

admin_bp = Blueprint("admin", __name__)

UPLOAD_FOLDER = "uploads"

# ----------------------------------------
# Download Encrypted Assignment (Admin)
# ----------------------------------------
@admin_bp.route("/download/<filename>", methods=["GET"])
@jwt_required()
@role_required("admin")
def download_assignment(filename):

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    with open(filepath, "rb") as f:
        encrypted = f.read()

    decrypted = decrypt_data(encrypted)

    return decrypted


# ----------------------------------------
# Differential Privacy Noise
# ----------------------------------------
import random
from decimal import Decimal

def add_noise(value, epsilon=1.0):

    # Handle NULL values
    if value is None:
        value = 0

    # Convert Decimal → float (CRITICAL FIX)
    if isinstance(value, Decimal):
        value = float(value)

    noise = random.uniform(-5, 5) / epsilon

    return round(value + noise, 2)




# ----------------------------------------
# FULL PLATFORM PRIVACY ANALYTICS
# ----------------------------------------
@admin_bp.route("/analytics", methods=["GET"])
@jwt_required()
@role_required("admin")
def analytics():

    db = get_db()
    cur = db.cursor(dictionary=True)

    analytics = {}

    import random

    # -----------------------------
    # Differential Privacy Helper
    # -----------------------------
    import random
    from decimal import Decimal

    def add_noise(value, epsilon=1.0):

        # Handle NULL values
        if value is None:
            value = 0

    # 🔧 Convert Decimal → float (CRITICAL)
        if isinstance(value, Decimal):
            value = float(value)

            noise = random.uniform(-5, 5) / epsilon

        return round(value + noise, 2)

    # -----------------------------
    # 1️⃣ Average Scores (DP)
    # -----------------------------
    cur.execute("""
        SELECT course, AVG(score) AS avg_score
        FROM learning_data
        WHERE score IS NOT NULL
        GROUP BY course
    """)

    avg_scores = {}

    for row in cur.fetchall():
        avg_scores[row["course"]] = add_noise(
            row["avg_score"]
        )

    analytics["average_scores"] = avg_scores

    # -----------------------------
    # 2️⃣ Totals
    # -----------------------------
    cur.execute("SELECT COUNT(*) AS total FROM quizzes")
    analytics["total_quizzes"] = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM doubts")
    analytics["total_doubts"] = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM study_posts")
    analytics["total_posts"] = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM study_posts
        WHERE video_url IS NOT NULL
        AND video_url != ''
    """)
    analytics["total_videos"] = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM assignments")
    analytics["assignments_uploaded"] = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM assignments
        WHERE marks IS NOT NULL
    """)
    analytics["assignments_graded"] = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM user_mapping
    """)
    analytics["active_users"] = cur.fetchone()["total"]

    # -----------------------------
    # 3️⃣ Course Engagement
    # -----------------------------
    cur.execute("""
        SELECT course, COUNT(*) AS learners
        FROM learning_data
        GROUP BY course
    """)
    analytics["course_engagement"] = cur.fetchall()

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return jsonify(analytics)

