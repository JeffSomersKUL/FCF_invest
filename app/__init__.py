from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'fcfinvest23@gmail.com'
app.config['MAIL_PASSWORD'] = 'fegva8-borGek-sesvag'

mail = Mail(app)

from app import routes