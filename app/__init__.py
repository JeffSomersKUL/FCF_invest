from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "7df08e95c64edebe39aef9f41a8e8780"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["MY_REACT_TARGET_VERSION"] = (
    "development"
    if os.getenv("ENVIRONMENT") == "development"
    else "production"
)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)


from app import models
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .context_processors import inject_config

app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
# Register the context processor
app.context_processor(inject_config)
