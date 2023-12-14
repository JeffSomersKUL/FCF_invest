from app import app, mail
import os
from flask import render_template, request
from flask import send_from_directory
from flask_mail import Mail, Message


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),'favicon.ico'
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/leadership")
def leadership():
    return render_template("leadership.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route('/submit_form', methods=['POST'])
def submit_form():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    subject = request.form.get('subject')
    content = request.form.get('content')

    # Process the form data (e.g., save to a database)

    print(f"Form submitted! First Name: {firstname},  Last Name: {lastname}, Email: {email}, Subject: {subject}, Content: {content}")

    send_email(subject, email, 'fcfinvest23@gmail.com', content)

    return render_template("index.html")

def send_email(subject, email, recipient, content):
    msg = Message(subject, sender=email, recipients=[recipient], body=content)

    try:
        mail.send(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')

