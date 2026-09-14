from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
csrf = CSRFProtect()
jwt = JWTManager()