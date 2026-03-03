from flask import Flask
from flask_cors import CORS
import os

from backend.extensions import mail, jwt, bcrypt
from auth.auth_routes import auth_bp
from auth.login import login_bp
from routes.student import student_bp
from routes.admin import admin_bp
from routes.instructor import instructor_bp

app = Flask(__name__)

# 🔐 Security
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret")
app.config["JWT_IDENTITY_CLAIM"] = "sub"

# 📧 Mail config
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME")
)

# 🔌 Init extensions
mail.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
CORS(app)

# 🧭 Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(login_bp, url_prefix="/auth")
app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(instructor_bp, url_prefix="/instructor")

@app.route("/")
def home():
    return "E-LEARNING PRIVACY BACKEND RUNNING"

if __name__ == "__main__":
    app.run(debug=False)
