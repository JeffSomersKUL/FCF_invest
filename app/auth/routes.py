from flask import render_template, jsonify
from .services import (
    get_member,
    send_confirmation_email,
    CONFIRM_STATE,
    SUCCESS_STATE,
    ERROR_STATE,
    EmailValidationError,
    EmailSendError,
)
from . import auth
from app import db, limiter
from app.models import User
from flask_login import login_user, current_user, login_required, logout_user
from flask_restful import reqparse
from flask_wtf.csrf import generate_csrf

signup_parser = reqparse.RequestParser()
signup_parser.add_argument(
    "email", type=str, required=True, help="Email is required"
)
signup_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)

signin_parser = signup_parser
signin_parser.add_argument(
    "email", type=str, required=True, help="Email is required"
)
signin_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)
signin_parser.add_argument("rememberMe", type=bool, required=False)

confirm_parser = reqparse.RequestParser()
confirm_parser.add_argument(
    "email", type=str, required=True, help="Email is required"
)
confirm_parser.add_argument(
    "code", type=str, required=True, help="Code is required"
)
confirm_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)


@auth.route("/login")
def login():
    return render_template(
        "login.html",
        token=generate_csrf(),
        confirm_state=CONFIRM_STATE,
        error_state=ERROR_STATE,
        success_state=SUCCESS_STATE,
    )


@auth.route("/profile")
@login_required
def profile():
    return render_template("profile.html", token=generate_csrf())


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({SUCCESS_STATE: "Logged out successfully"}), 200


@auth.route("/signup", methods=["POST"])
def signup():
    args = signup_parser.parse_args()
    email = args.email
    psw = args.password

    if current_user.is_authenticated:
        return jsonify({ERROR_STATE: "Already logged in"}), 400

    try:
        member = get_member(email)
    except EmailValidationError as e:
        return jsonify({ERROR_STATE: e.message}), 400

    user = User(email=email, member_id=member.id)
    user.set_password(psw)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({ERROR_STATE: "Database operation failed"}), 400
    try:
        send_confirmation_email(user)
    except EmailSendError as e:
        return jsonify({ERROR_STATE: e.message}), 400

    return jsonify({CONFIRM_STATE: email}), 201


@auth.route("/signin", methods=["POST"])
def signin():
    args = signin_parser.parse_args()
    email = args.email
    psw = args.password
    remember_me = args.rememberMe

    if current_user.is_authenticated:
        return jsonify({ERROR_STATE: "Already logged in"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(psw):
        if user.confirmed:
            login_user(user, remember=remember_me)
            return jsonify({SUCCESS_STATE: "Logged in successfully"}), 200
        else:
            return jsonify({CONFIRM_STATE: email}), 201
    return jsonify({ERROR_STATE: "Invalid email or password"}), 400


@auth.route("/verify-email", methods=["POST"])
def verify_confirmation_code():
    args = confirm_parser.parse_args()
    email = args.email
    code = args.code
    password = args.password

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        if user.confirmed:
            login_user(user)
            return (
                jsonify({SUCCESS_STATE: "Email confirmed successfully"}),
                200,
            )
        if user and user.confirmation_code == code:
            user.confirmed = True
            user.confirmation_code = (
                None  # Clear the code after successful confirmation
            )
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({ERROR_STATE: "Database operation failed"}), 400
            login_user(user)
            return (
                jsonify({SUCCESS_STATE: "Email confirmed successfully"}),
                200,
            )
        return jsonify({ERROR_STATE: "Invalid confirmation code"}), 400
    else:
        return jsonify({ERROR_STATE: "Invalid email or password"}), 400


@auth.route("/resend-confirmation", methods=["POST"])
@limiter.limit("5 per day")
def send_confirm():
    args = signup_parser.parse_args()
    email = args.email
    password = args.password

    if current_user.is_authenticated:
        return jsonify({ERROR_STATE: "Already logged in"}), 400

    user = User.query.filter_by(email=email).first()

    if not user and user.check_password(password) and user.confirmed:
        return jsonify({ERROR_STATE: "Can't resend"}), 400
    try:
        send_confirmation_email(user)
    except EmailSendError as e:
        return jsonify({ERROR_STATE: e.message}), 400

    return jsonify({CONFIRM_STATE: email}), 201


@auth.errorhandler(429)
def ratelimit_handler(e):
    return {
        ERROR_STATE: "You reached your limit to resend confirmation emails"
    }, 400
