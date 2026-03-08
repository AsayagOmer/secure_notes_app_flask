import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_cipher():
    # Retrieve the SECRET_KEY from the environment to generate a strong AES key
    secret_key = os.environ.get('SECRET_KEY', 'default_dev_key').encode()

    # Use PBKDF2 for Key Stretching
    # This process makes the key significantly more resistant to Brute Force attacks
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'secure_notes_static_salt_v1',  # In production, use a unique, per-user salt
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(secret_key))
    return Fernet(key)


def encrypt_text(plain_text: str) -> str:
    """Encrypts plain text and returns an encrypted string."""
    if not plain_text:
        return plain_text

    cipher = get_cipher()
    # Fernet (AES) requires bytes, so we encode the text to utf-8
    return cipher.encrypt(plain_text.encode('utf-8')).decode('utf-8')


def decrypt_text(encrypted_text: str) -> str:
    """Decrypts an encrypted string back to plain text."""
    if not encrypted_text:
        return encrypted_text

    cipher = get_cipher()
    return (cipher.decrypt(encrypted_text.encode('utf-8'))
            .decode('utf-8'))