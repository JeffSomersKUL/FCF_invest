from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = '7df08e95c64edebe39aef9f41a8e8780'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') 

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

from app import routes, models