from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

mail = Mail()
jwt = JWTManager()
bcrypt = Bcrypt()
