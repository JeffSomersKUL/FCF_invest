import os
import sys
import logging
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
from flask_ckeditor import CKEditor
from flask_restful import Api
from logging.handlers import RotatingFileHandler

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["ENVIRONMENT"] = (
    "development" if os.getenv("ENVIRONMENT") == "development" else "production"
)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["VITE_ORIGIN"] = "http://localhost:5173"
app.config["UPLOAD_PATH_IMAGES"] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "upload/images"
)
app.config["CKEDITOR_PKG_TYPE"] = "full"
app.config["CKEDITOR_FILE_UPLOADER"] = "upload.file_upload"
app.config["CKEDITOR_ENABLE_CSRF"] = True
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
app.config["LOG_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "logs")
app.config["SCHEDULER_LOG_FILE"] = os.path.join(app.config["LOG_DIR"], "scheduler.log")
app.config["FLASK_LOG_FILE"] = os.path.join(app.config["LOG_DIR"], "flask.log")

# Ensure the paths exists
if not os.path.exists(app.config["UPLOAD_PATH_IMAGES"]):
    os.makedirs(app.config["UPLOAD_PATH_IMAGES"])
if not os.path.exists(app.config["LOG_DIR"]):
    os.makedirs(app.config["LOG_DIR"])


# FLASK LOG
# custom logger for scheduler
flask_file_handler = RotatingFileHandler(
    app.config["FLASK_LOG_FILE"], maxBytes=1000000, backupCount=5
)
flask_file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
flask_file_handler.setFormatter(formatter)

flask_logger = logging.getLogger("flask_app")
flask_logger.setLevel(logging.INFO)
flask_logger.addHandler(flask_file_handler)

flask_console_handler = logging.StreamHandler(sys.stdout)
flask_console_handler.setLevel(logging.INFO)
flask_console_handler.setFormatter(formatter)
flask_logger.addHandler(flask_console_handler)


# SHEDULER LOG
# custom logger for scheduler
file_handler = RotatingFileHandler(
    app.config["SCHEDULER_LOG_FILE"], maxBytes=1000000, backupCount=5
)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)


# Scheduler logger
scheduler_logger = logging.getLogger("scheduler")
scheduler_logger.setLevel(logging.INFO)
scheduler_logger.addHandler(file_handler)

# Capture warnings and redirect them to the logging system
logging.captureWarnings(True)

# Get the 'py.warnings' logger and add the scheduler file handler
py_warnings_logger = logging.getLogger("py.warnings")
py_warnings_logger.setLevel(logging.INFO)
py_warnings_logger.addHandler(file_handler)

# Configure the 'apscheduler' logger
apscheduler_logger = logging.getLogger("apscheduler")
apscheduler_logger.setLevel(logging.INFO)
apscheduler_logger.addHandler(file_handler)

# Configure the 'numexpr' logger (if NumExpr uses logging)
numexpr_logger = logging.getLogger("numexpr")
numexpr_logger.setLevel(logging.INFO)
numexpr_logger.addHandler(file_handler)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
mail = Mail(app)
limiter = Limiter(get_remote_address, app=app)
ckeditor = CKEditor(app)
api = Api(app)


from .main import main as main_blueprint
from .portfolio import portfolio as portfolio_blueprint
from .auth import auth as auth_blueprint
from .context_processors import inject_config
from .admin import admin_bp, create_admin
from .assets_blueprint import frontend_blueprint
from .upload import upload_blueprint
from .scheduler import init_scheduler

init_scheduler(app)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(portfolio_blueprint, url_prefix="/portfolio")
create_admin(app)
app.register_blueprint(admin_bp)
app.register_blueprint(frontend_blueprint)
app.register_blueprint(upload_blueprint)
# Register the context processor
app.context_processor(inject_config)
