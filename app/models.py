from app.extensions import db
from flask_login import UserMixin

from app.encryption import encrypt_text, decrypt_text
from cryptography.fernet import InvalidToken

import pyotp

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    # relation one-to-many: One user, many notes
    notes = db.relationship('Note', backref='author', lazy=True)

    # --- MFA Extensions ---
    otp_secret = db.Column(db.String(32))
    is_mfa_enabled = db.Column(db.Boolean, default=False)

    def get_totp_uri(self):
        """
        Generates the URI used to create a QR code for authenticator apps.
        """
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(
            name=self.username,  # If your column is named 'email', change this to self.email
            issuer_name="SecureNotesApp"
        )

    def verify_totp(self, token):
        """
        Validates the 6-digit code provided by the user.
        """
        totp = pyotp.totp.TOTP(self.otp_secret)
        return totp.verify(token)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    # 1. The actual database column (hidden from the application layer)
    # We refer to it as _content in Python, but it is stored as 'content' in the table.
    _content = db.Column('content', db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 2. Getter: Triggered when the application wants to READ the note content
    @property
    def content(self):
        try:
            return decrypt_text(self._content)
        except InvalidToken:
            # Fallback: If decryption fails, it's likely a legacy note (pre-encryption).
            # Return it as-is to prevent the application from crashing.
            return self._content
        except Exception:
            return "🔒 [Decryption Error: Content corrupted or secret key mismatch]"

    # 3. Setter: Triggered when the application wants to SAVE/UPDATE note content
    @content.setter
    def content(self, value):
        # Automatically encrypt the value before storing it in the database
        self._content = encrypt_text(value)