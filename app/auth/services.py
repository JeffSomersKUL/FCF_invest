import os
from flask import render_template, current_app
from app.models import User, Member
from app import mail, db
from flask_mail import Message

CONFIRM_STATE = "confirm"
SUCCESS_STATE = "success"
ERROR_STATE = "error"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def is_valid_email(email):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        if existing_user.confirmed:
            return {ERROR_STATE: "User with this email already exists"}, 400
        else:
            return {
                ERROR_STATE: "User already signed up, but confirmation is needed"
            }, 400
    # check if it is a member
    allowed_member = Member.query.filter_by(current=True, email=email).first()
    if not allowed_member:
        return {ERROR_STATE: "You are not a member"}, 400

    return allowed_member


def send_email(to, subject, template, attachments=[]):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_USERNAME"],
    )
    for att in attachments:
        with open(att, "rb") as img:
            msg.attach(
                "my_image.png",
                "image/png",
                img.read(),
                "inline",
                headers=[["Content-ID", "<logo>"]],
            )
    mail.send(msg)


def send_confirmation_email(user):
    if user.confirmed:
        return {ERROR_STATE: "Email already confirmed"}, 400
    user.generate_confirmation_code()
    db.session.commit()

    # Base64 encode the logo image
    path_logo = os.path.join(
        os.path.dirname(BASE_DIR),
        "static",
        "images",
        "logos",
        "fcf-logo-blue.png",
    )

    html = render_template(
        "mail/activate.html",
        confirmation_code=user.confirmation_code,
    )
    subject = "Please confirm your email"
    try:
        send_email(user.email, subject, html, attachments=[path_logo])
    except Exception as e:
        print(e)
        return {ERROR_STATE: "Email operation failed"}, 400
    return None
