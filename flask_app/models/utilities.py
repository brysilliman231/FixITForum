from flask import session, redirect, url_for, flash
from functools import wraps

def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("You must be logged in to access this page.")
                return redirect(url_for('login')) 
            return f(*args, **kwargs)
        return decorated_function