from flask import render_template, jsonify
from . import auth
from app import db
from app.models import User, AllowedEmail
from flask_login import login_user, current_user, login_required, logout_user
from flask_restful import reqparse
from flask_wtf.csrf import generate_csrf


@auth.route("/login")
def login():
    return render_template("login.html", token=generate_csrf())


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"success": "Logged out successfully"}), 200


@auth.route("/profile")
@login_required
def profile():
    return render_template("profile.html", token=generate_csrf())


def check_valid_email(email):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "User with this email already exists"}, 400

    allowed_emails = AllowedEmail.query.all()
    emails = [e.email for e in allowed_emails]
    if email not in emails:
        return {"error": "Not allowed email"}, 400

    return None


signup_parser = reqparse.RequestParser()
signup_parser.add_argument(
    "firstname", type=str, required=True, help="First name is required"
)
signup_parser.add_argument(
    "lastname", type=str, required=True, help="Last name is required"
)
signup_parser.add_argument(
    "email", type=str, required=True, help="Email is required"
)
signup_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)


@auth.route("/signup", methods=["POST"])
def signup():
    args = signup_parser.parse_args()
    error_response = check_valid_email(args.email)
    if error_response:
        return jsonify(error_response[0]), error_response[1]

    user = User(fname=args.firstname, lname=args.lastname, email=args.email)
    user.set_password(args.password)

    db.session.add(user)  # TODO try catch rond zetten als er iets fout loopt
    db.session.commit()

    login_user(user)

    return jsonify({"success": "User created successfully"}), 201


signin_parser = reqparse.RequestParser()
signin_parser.add_argument(
    "email", type=str, required=True, help="Email is required"
)
signin_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)
signin_parser.add_argument("rememberMe", type=bool, required=False)


@auth.route("/signin", methods=["POST"])
def signin():
    args = signin_parser.parse_args()
    email = args.email
    psw = args.password
    remember_me = args.rememberMe

    if current_user.is_authenticated:
        return jsonify({"error": "Already logged in"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(psw):
        login_user(user, remember=remember_me)
        return jsonify({"success": "Logged in successfully"}), 200
    return jsonify({"error": "Invalid email or password"}), 400
