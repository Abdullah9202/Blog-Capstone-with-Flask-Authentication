from functools import wraps
from flask import abort
# My Files (main.py)
from flask_login import current_user

# Creating the admin access only function
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Validating the user
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue the route function
        return f(*args, **kwargs)
    return decorated_function