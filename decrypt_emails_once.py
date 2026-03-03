"""
ONE-TIME ADMIN SCRIPT
Decrypts all encrypted emails from users_identity table

⚠️ Do NOT commit this file
⚠️ Run only in secure local environment
"""

from backend.database import get_db
from privacy.encryption import decrypt_data


def decrypt_all_emails():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, email FROM users_identity")
    users = cursor.fetchall()

    print("\n=== DECRYPTED EMAILS (ADMIN ONLY) ===\n")

    for user in users:
        try:
            encrypted_email = user["email"]

            # Fernet expects bytes
            if isinstance(encrypted_email, str):
                encrypted_email = encrypted_email.encode()

            decrypted_email = decrypt_data(encrypted_email)

            print(f"User ID: {user['id']}  |  Email: {decrypted_email}")

        except Exception as e:
            print(f"User ID: {user['id']}  |  ERROR decrypting email: {e}")

    cursor.close()
    db.close()


if __name__ == "__main__":
    decrypt_all_emails()
