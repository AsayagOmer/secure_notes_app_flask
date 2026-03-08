import os
from app import create_app

print("=== STARTING APP INITIALIZATION ===", flush=True)

# 1. Let's print which variables Python actually sees (without printing the actual password)
db_url = os.environ.get('DATABASE_URL')
flask_env = os.environ.get('FLASK_ENV')
print(f"DEBUG - FLASK_ENV is: {flask_env}", flush=True)
print(f"DEBUG - DATABASE_URL is set: {db_url is not None}", flush=True)

# 2. Force the system into Production mode if a DATABASE_URL is present
if db_url and not os.environ.get('FLASK_CONFIG'):
    print("DEBUG - Forcing Production config because DATABASE_URL is present", flush=True)
    os.environ['FLASK_CONFIG'] = 'production'

config_name = os.getenv('FLASK_CONFIG') or 'default'
print(f"DEBUG - Using config: {config_name}", flush=True)

# 3. App creation (this is usually where crashes occur)
app = create_app(config_name)

print("=== APP INITIALIZATION SUCCESSFUL ===", flush=True)

if __name__ == '__main__':
    app.run()