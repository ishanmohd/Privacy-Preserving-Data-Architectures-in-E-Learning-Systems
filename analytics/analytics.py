from backend.database import get_db
import random

# -----------------------------
# Differential Privacy Noise
# -----------------------------
def add_noise(value, epsilon=1.0):
    noise = random.uniform(-5, 5) / epsilon
    return round(value + noise, 2)

# -----------------------------
# FULL PLATFORM ANALYTICS
# -----------------------------
def full_admin_analytics():

    db = get_db()
    cur = db.cursor(dictionary=True)

    # -------------------------
    # 1️⃣ Quiz Analytics
    # -------------------------
    cur.execute("SELECT COUNT(*) AS total FROM quizzes")
    total_quizzes = cur.fetchone()["total"]

    # -------------------------
    # 2️⃣ Doubts
    # -------------------------
    cur.execute("SELECT COUNT(*) AS total FROM doubts")
    total_doubts = cur.fetchone()["total"]

    # -------------------------
    # 3️⃣ Study Posts
    # -------------------------
    cur.execute("SELECT COUNT(*) AS total FROM study_posts")
    total_posts = cur.fetchone()["total"]

    # -------------------------
    # 4️⃣ Video Lectures
    # -------------------------
    cur.execute("""
        SELECT COUNT(*) AS total
        FROM study_posts
        WHERE video_url IS NOT NULL
    """)
    total_videos = cur.fetchone()["total"]

    # -------------------------
    # 5️⃣ Assignments Uploaded
    # -------------------------
    cur.execute("SELECT COUNT(*) AS total FROM assignments")
    assignments_uploaded = cur.fetchone()["total"]

    # -------------------------
    # 6️⃣ Assignments Graded
    # -------------------------
    cur.execute("""
        SELECT COUNT(*) AS total
        FROM assignments
        WHERE marks IS NOT NULL
    """)
    assignments_graded = cur.fetchone()["total"]

    # -------------------------
    # 7️⃣ Active Learners
    # -------------------------
    cur.execute("""
        SELECT COUNT(*) AS total
        FROM users_identity
        WHERE role='student'
    """)
    active_users = cur.fetchone()["total"]

    # -------------------------
    # 8️⃣ Privacy-Safe Scores
    # -------------------------
    cur.execute("""
        SELECT course, AVG(score) AS avg_score
        FROM learning_data
        GROUP BY course
    """)

    avg_scores = {}

    for row in cur.fetchall():
        avg_scores[row["course"]] = add_noise(
            row["avg_score"] or 0
        )

    # -------------------------
    # 9️⃣ Course Engagement
    # -------------------------
    cur.execute("""
        SELECT course,
        COUNT(DISTINCT pseudo_id) AS learners
        FROM learning_data
        GROUP BY course
    """)

    engagement = cur.fetchall()

    # -------------------------
    # FINAL JSON
    # -------------------------
    return {
        "average_scores": avg_scores,
        "total_quizzes": total_quizzes,
        "total_doubts": total_doubts,
        "total_posts": total_posts,
        "total_videos": total_videos,
        "assignments_uploaded": assignments_uploaded,
        "assignments_graded": assignments_graded,
        "active_users": active_users,
        "course_engagement": engagement
    }
