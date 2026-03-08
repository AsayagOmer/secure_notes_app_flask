from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import db

import pyotp
import qrcode
import base64
from io import BytesIO

# Define the 'auth' Blueprint.
# This name will be used for routing, e.g., url_for('auth.login')
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    GET: Displays the registration form.
    POST: Hashes the password, saves the new user to the database, and redirects to login.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hash the password for security using pbkdf2
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password_hash=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    GET: Displays the login form.
    POST: Validates user credentials and initiates a session if successful.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        # Verify if user exists and the password hash matches
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # Redirect to the notes index page upon successful login
            return redirect(url_for('notes.index'))

        flash('Invalid username or password', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Log out the current user and redirect them to the login page.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/setup-mfa', methods=['GET', 'POST'])
@login_required
def setup_mfa():
    try:
        # If the user already has MFA enabled, redirect them
        if current_user.is_mfa_enabled:
            flash('MFA is already enabled on your account.', 'info')
            return redirect(url_for('notes.index'))

        if request.method == 'GET':
            # 1. Generate a new secret if one doesn't exist yet
            if not current_user.otp_secret:
                current_user.otp_secret = pyotp.random_base32()
                db.session.commit()

            # 2. Generate the QR code
            uri = current_user.get_totp_uri()
            img = qrcode.make(uri)

            # 3. Save the image to a memory buffer and encode it to Base64 for the HTML template
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            return render_template('setup_mfa.html', qr_code=qr_base64, secret=current_user.otp_secret)

        elif request.method == 'POST':
            # 4. The user scanned the code and entered the 6-digit token - let's verify it!
            token = request.form.get('token')
            if current_user.verify_totp(token):
                current_user.is_mfa_enabled = True
                db.session.commit()
                flash('MFA setup complete! Your account is now secured.', 'success')
                return redirect(url_for('notes.index'))
            else:
                flash('Invalid code. Please try again.', 'danger')
                return redirect(url_for('auth.setup_mfa'))

    except Exception as e:
        # I'll try to catch the error to my screen.
        import traceback
        return f"<h1>Oops! Here is the exact error:</h1><pre style='background:#f4f4f4; padding:20px; font-size:16px;'>{traceback.format_exc()}</pre>", 500