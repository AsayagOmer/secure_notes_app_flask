
# 🔒 Secure Notes App

A secure, modular, and production-ready web application for managing personal notes. Built with **Python** and **Flask**, this project leverages the Application Factory pattern, Blueprints, and MVC architecture to ensure a scalable and maintainable codebase.

<div align="center">
  <img src="./readme_images/MVC.jpg" width="550" height="300" alt="MVC Architecture Diagram">
</div>

## 🔨 System Architecture

<div align="left">
  <img src="./readme_images/system_archicture.png" width="850" height="550" alt="MVC Architecture Diagram">
</div>

## ✨ Key Features & Security

* **Robust Architecture:** Implements the Application Factory pattern and Flask Blueprints for clean separation of concerns between authentication (`auth`) and core functionality (`notes`).
<p></p>

* **Secure Authentication:** Full user registration, login, and session management handling via `Flask-Login` and secure password hashing.
<p></p>

* **Form & CSRF Protection:** Integrated `Flask-WTF` to secure all web forms against Cross-Site Request Forgery (CSRF) attacks.
<p></p>

* **Database Management:** Utilizes `Flask-SQLAlchemy` for ORM capabilities, with `psycopg2` integrated for robust PostgreSQL database support in production.
<p></p>

* **Production-Ready:** Configured to run with `Gunicorn` as the WSGI HTTP Server.
<p></p>

* **Container Orchestration:** Includes Kubernetes (`k8s`) manifests for seamless cloud deployment and scaling.
<p></p>

* **CI/CD Integrated:** Automated pipelines configured via GitHub Actions.

## 📁 Repository Structure

The project is structured for scalability and clear environment management:

```text
SecureFlaskApp/
├── .github/               
│   └── workflows/         # CI/CD pipelines (GitHub Actions)
├── app/                   # Core application package
│   ├── auth/              # Authentication Blueprint
│   ├── notes/             # Notes management Blueprint
│   ├── static/            # CSS, JS, and image assets
│   └── templates/         # Jinja2 HTML templates
├── instance/              # Environment-specific files (e.g., local SQLite DB)
├── k8s/                   # Kubernetes deployment and service manifests
├── readme_images/         # Documentation assets
├── .env                   # Environment variables (excluded from version control)
├── requirements.txt       # Project dependencies
└── run.py                 # Application entry point

```

## 🚀 Local Development Setup

Follow these steps to run the application on your local machine.

**1. Clone the repository:**

```bash
git clone [https://github.com/AsayagOmer/secure_notes_app_flask.git](https://github.com/AsayagOmer/secure_notes_app_flask.git)
cd secure_notes_app_flask

```

**2. Create and activate a virtual environment:**

* Windows:
```bash
python -m venv .venv
.venv\Scripts\activate

```


* Mac/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate

```



**3. Install dependencies:**

```bash
pip install -r requirements.txt

```

**4. Configure Environment Variables:**
Create a `.env` file in the root directory. You can use this to set your database URI, secret keys, and Flask environment.

**5. Run the application:**
For local development:

```bash
flask run

```

For production testing (using Gunicorn):

```bash
gunicorn -w 4 -b 127.0.0.1:5000 run:app

```

## ☸️ Kubernetes Deployment

This project is ready to be deployed to a Kubernetes cluster. Navigate to the `k8s/` directory and apply the configuration files to your cluster:

```bash
kubectl apply -f k8s/

```

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend** | Python 3, Flask, Gunicorn |
| **Database** | SQLAlchemy, PostgreSQL (`psycopg2`), SQLite (local) |
| **Security** | Flask-WTF, Flask-Login, Werkzeug Security, `python-dotenv` |
| **Frontend** | HTML5, CSS3, Jinja2 |
| **DevOps** | Kubernetes, GitHub Actions |


