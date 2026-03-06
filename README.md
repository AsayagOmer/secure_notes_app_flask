# Project Structure: Secure Notes App

This document outlines the directory structure and the purpose of each component within the Flask application.

## Directory Tree

```text
secure_notes_app/
├── run.py                 # Application entry point
├── config.py              # Environment configurations (Dev/Prod/Test)
└── app/                   # Main application package
    ├── __init__.py        # Application Factory initialization
    ├── extensions.py      # Global objects (DB, CSRF) to prevent circular imports
    ├── models.py          # Database models and schema definitions
    ├── auth/              # Authentication Blueprint
    │   ├── __init__.py
    │   └── routes.py
    ├── notes/             # Notes management Blueprint
    │   ├── __init__.py
    │   └── routes.py
    └── templates/         # HTML templates