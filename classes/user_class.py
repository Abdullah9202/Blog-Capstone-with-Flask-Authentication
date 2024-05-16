from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, URL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# My Files (Classes)
from classes.blogPost import db

# Declarative Base for Mapped Classes
Base = declarative_base()

# Custom Password Validation can be created for the login and registeration forms

# Register Form Class (Flask Form)
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up!")
    
# Login Form Class (Flask Form)
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")

# User Class (DB)
class User(UserMixin, db.Model, Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Defining one to many relationships with posts
    posts = relationship("Posts", back_populates="user")