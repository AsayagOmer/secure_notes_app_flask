import os
from flask import Flask
from config import config_dict
from app.extensions import db, csrf, login_manager


def create_app(config_name='development'):
    """
    Initialize and configure the Flask application.
    This factory function sets up the database, security extensions,
    login management, and registers application blueprints.
    """
    app = Flask(__name__)

    # Load settings from the configuration dictionary
    app.config.from_object(config_dict[config_name])

    # --- CRITICAL FIX: Direct Injection of Database URL ---
    # Retrieve the database URL injected into the pod (e.g., by Kubernetes)
    db_url = os.environ.get('DATABASE_URL')

    if db_url:
        # Resolve known SQLAlchemy/PostgreSQL compatibility issue:
        # SQLAlchemy requires 'postgresql://' while some providers use 'postgres://'
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        # Override the Flask internal configuration with the safe URL
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    # -----------------------------------------------------------

    # Initialize extensions and bind them to the app instance
    # This will now initialize correctly as the URI is guaranteed.
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Define the default login view for unauthorized users
    login_manager.login_view = 'auth.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        """
        Callback used by Flask-Login to reload the user object from the user ID
        stored in the session.
        """
        return User.query.get(int(user_id))

    # Register Blueprints for different modules (Auth and Notes)
    from app.auth.routes import auth_bp
    from app.notes.routes import notes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    # Ensure database tables are created within the application context
    # (Primarily used for development and testing environments)
    with app.app_context():
        db.create_all()

    return app