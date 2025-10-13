from flask import render_template, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from flask_restful import reqparse
from flask_restful import Resource

from . import auth
from app import db, limiter
from app.user.models import User
from .services import (
    get_member,
    send_confirmation_email,
    CONFIRM_STATE,
    SUCCESS_STATE,
    ERROR_STATE,
    EmailValidationError,
    EmailSendError,
)


@auth.route("/login")
def login():
    return render_template(
        "login.html",
        confirm_state=CONFIRM_STATE,
        error_state=ERROR_STATE,
        success_state=SUCCESS_STATE,
    )


@auth.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


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


class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {SUCCESS_STATE: "Logged out successfully"}, 200


class Signup(Resource):
    def post(self):
        args = signup_parser.parse_args()
        email = args.email
        psw = args.password

        if current_user.is_authenticated:
            return {ERROR_STATE: "Already logged in"}, 400

        try:
            member = get_member(email)
        except EmailValidationError as e:
            return {ERROR_STATE: e.message}, 400

        user = User(email=email, member_id=member.id)
        user.set_password(psw)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            return {ERROR_STATE: "Database operation failed"}, 400
        try:
            send_confirmation_email(user)
        except EmailSendError as e:
            return {ERROR_STATE: e.message}, 400

        return {CONFIRM_STATE: email}, 201


class Signin(Resource):
    def post(self):
        args = signin_parser.parse_args()
        email = args.email
        psw = args.password
        remember_me = args.rememberMe

        if current_user.is_authenticated:
            return {ERROR_STATE: "Already logged in"}, 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(psw):
            if user.confirmed:
                login_user(user, remember=remember_me)
                return {SUCCESS_STATE: "Logged in successfully"}, 200
            else:
                return jsonify({CONFIRM_STATE: email}), 201
        return {ERROR_STATE: "Invalid email or password"}, 400


class VerifyEmail(Resource):
    def post(self):
        args = confirm_parser.parse_args()
        email = args.email
        code = args.code
        password = args.password

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if user.confirmed:
                login_user(user)
                return (
                    {SUCCESS_STATE: "Email confirmed successfully"},
                    200,
                )
            if user and user.confirmation_code == code:
                user.confirmed = True
                user.confirmation_code = None
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    return (
                        {ERROR_STATE: "Database operation failed"},
                        400,
                    )
                login_user(user)
                return (
                    {SUCCESS_STATE: "Email confirmed successfully"},
                    200,
                )
            return {ERROR_STATE: "Invalid confirmation code"}, 400
        return {ERROR_STATE: "Invalid email or password"}, 400


class ResendConfirmation(Resource):
    @limiter.limit("5 per day")
    def post(self):
        args = signup_parser.parse_args()
        email = args.email
        password = args.password

        if current_user.is_authenticated:
            return {ERROR_STATE: "Already logged in"}, 400

        user = User.query.filter_by(email=email).first()

        if not user and user.check_password(password) and user.confirmed:
            return {ERROR_STATE: "Can't resend"}, 400
        try:
            send_confirmation_email(user)
        except EmailSendError as e:
            return {ERROR_STATE: e.message}, 400

        return {CONFIRM_STATE: email}, 201


@auth.errorhandler(429)
def ratelimit_handler(e):
    return {
        ERROR_STATE: "You reached your limit to resend confirmation emails"
    }, 400
