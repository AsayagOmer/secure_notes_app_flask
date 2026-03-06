import os
from app import create_app

# Take the environment from .env file (or a default value of development)
config_name = os.environ.get('FLASK_ENV', 'development')

app = create_app(config_name)

if __name__ == '__main__':
    # Operates the server (the DEBUG in config)
    app.run()