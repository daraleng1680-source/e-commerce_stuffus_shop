from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from model import User
    
    # Handle GET request - show login form
    if request.method == 'GET':
        return render_template('login/index.html')
    
    # Handle POST request - process login
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    # Validate input
    if not username or not password:
        return render_template('login/index.html', error='Username and password are required')
    
    # Query user from database
    user = User.query.filter_by(username=username).first()
    
    # Check if user exists and password is correct
    if user and password:
        password_valid = False
        
        try:
            # Try hash verification first
            password_valid = check_password_hash(user.password, password)
        except Exception:
            password_valid = False
        
        # Fallback: check plaintext password for legacy support
        if not password_valid and user.password == password:
            password_valid = True
        
        if password_valid:
            # Create permanent session
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['profile'] = user.profile
            flash(f"Welcome {user.username}!", "success")
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('admin.dashboard_route'))
    
    # Failed login - return to login form with error
    flash('Invalid username or password', 'danger')
    return render_template('login/index.html', error='Invalid username or password')
