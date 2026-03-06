import os
from dotenv import load_dotenv

# Load variables from the .env file into the Python environment
load_dotenv()


# Base class with settings shared across all environments
class Config:
    # If the variable doesn't exist in .env, use a fallback (not recommended for production!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Development environment (your local machine)
class DevelopmentConfig(Config):
    DEBUG = True
    # Use a local SQLite database for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///notes_dev.db'


# Production environment (the live server)
class ProductionConfig(Config):
    DEBUG = False
    # In production, the database connection must be secure and external
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    db_url = SQLALCHEMY_DATABASE_URI
    # Old format fix: for Render
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)

    # Stricter security settings for production environments
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


# Testing environment (for Unit Tests)
class TestingConfig(Config):
    TESTING = True
    # In-memory database - wiped clean after tests finish
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Disable CSRF during tests to simplify automated testing
    WTF_CSRF_ENABLED = False


# Dictionary to help retrieve the correct configuration class by name
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}