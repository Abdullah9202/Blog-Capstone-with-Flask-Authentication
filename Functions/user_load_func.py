from flask_login import LoginManager
# My Files (Classes)
from classes.user_class import User_db, User

login_Manager = LoginManager()

# User loader function
@login_Manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)