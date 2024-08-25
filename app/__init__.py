from flask import Flask, send_from_directory
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["ENVIRONMENT"] = (
    "development"
    if os.getenv("ENVIRONMENT") == "development"
    else "production"
)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["VITE_ORIGIN"] = "http://localhost:5173"
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
mail = Mail(app)
# Set up Flask-Limiter
limiter = Limiter(get_remote_address, app=app)

from app import models
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .context_processors import inject_config
from .admin import admin_bp, create_admin
from .assets_blueprint import frontend_blueprint


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"), "favicon.ico"
    )


app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
create_admin(app)
app.register_blueprint(admin_bp)
app.register_blueprint(frontend_blueprint)
# Register the context processor
app.context_processor(inject_config)
