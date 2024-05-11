from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

User_db = SQLAlchemy()

# User Class
class User(UserMixin, User_db.Model):
    __tablename__ = "registered_users"
    id = User_db.column(User_db.Integer, primary_key=True)
    name = User_db.column(User_db.String(1000), nullable=False)
    email = User_db.column(User_db.String(100), unique=True, nullable=False)
    password = User_db.column(User_db.String(100), nullable=False)