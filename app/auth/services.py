import os
import re
import mimetypes
from flask import render_template, current_app

from app.models import User, Member
from app import mail, db
from flask_mail import Message

CONFIRM_STATE = "confirm"
SUCCESS_STATE = "success"
ERROR_STATE = "error"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class EmailValidationError(Exception):
    """Custom exception for email validation errors."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class EmailSendError(Exception):
    """Custom exception for email sending."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def get_member(email):
    # Basic email format validation using regex
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if not re.match(email_regex, email):
        raise EmailValidationError("Invalid email format")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        if existing_user.confirmed:
            raise EmailValidationError("User with this email already exists")
        else:
            raise EmailValidationError(
                "User with this email already signed up, but not confirmed"
            )

    allowed_member = Member.query.filter_by(current=True, email=email).first()

    if not allowed_member:
        raise EmailValidationError("Email not associated with a valid member")

    # If everything is valid, return the member
    return allowed_member


def send_email(to, subject, template, attachments=[]):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_USERNAME"],
    )
    for att in attachments:
        try:
            with open(att, "rb") as f:
                file_name = att.split("/")[-1]
                mime_type, _ = mimetypes.guess_type(att)

                if mime_type is None:
                    mime_type = "application/octet-stream"  # Default MIME type

                # msg.attach(
                #     filename=file_name,
                #     content_type=mime_type,
                #     data=f.read(),
                #     disposition="inline",
                #     headers=[["Content-ID", f"<{file_name}>"]],
                # )
        except IOError:
            raise EmailSendError(f"Error reading file {att}")
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
        raise EmailSendError("Email operation failed")
