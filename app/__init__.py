from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'fcfinvest23@gmail.com'
app.config['MAIL_PASSWORD'] = 'fegva8-borGek-sesvag'
app.config['SECRET_KEY'] = '7df08e95c64edebe39aef9f41a8e8780'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

from app import routes, models