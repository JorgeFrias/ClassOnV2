from flask import flash, redirect, url_for, session
from functools import wraps

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('home.login'))
    return wrap

def is_logged_in_professor(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and 'isProfessor' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('home.login'))
    return wrap

def defined_session(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'id_class' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please create classroom session', 'danger')
            return redirect(url_for('professor.dashboard'))
    return wrap