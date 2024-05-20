from app import app, db
import os
from flask import render_template, request, redirect, url_for, jsonify
from flask import send_from_directory
from flask_login import login_user, current_user, login_required, logout_user
from flask_restful import reqparse
from .models import ContactFormData, User, AllowedEmail
from .forms import ContactForm
from sqlalchemy.exc import SQLAlchemyError
from flask_wtf.csrf import generate_csrf


@app.context_processor
def inject_config():
    filtered_config = {
        k: v for k, v in app.config.items() if k.startswith("MY_")
    }
    return dict(config=filtered_config)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"), "favicon.ico"
    )


@app.route("/")
def index():
    form = ContactForm(request.form)
    return render_template("home.html", form=form)


@app.route("/about/leadership")
def leadership():
    return render_template("leadership.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    form = ContactForm(request.form)

    if form.validate():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        subject = form.subject.data
        content = form.content.data

        print(
            f"Form received! First Name: {fname},  Last Name: {lname}, Email: {email}, Subject: {subject}, Content: {content}"
        )
        form_data = ContactFormData(
            fname=fname,
            lname=lname,
            email=email,
            subject=subject,
            content=content,
        )
        try:
            db.session.add(form_data)
            db.session.commit()
            return {"response": "success"}
        except SQLAlchemyError:
            db.session.rollback()
            return {"response": "failed"}
    else:
        return {"response": list(form.errors.keys())}


@app.route("/cc7fccf50f9946b1e93dcc29946b13ef")
def view_messages():
    messages = ContactFormData.query.all()

    return render_template("messages.html", messages=messages)


@app.route("/delete_message/<int:message_id>")
def delete_message(message_id):
    message = ContactFormData.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
    return redirect(url_for("view_messages"))


@app.route("/login")
def login():
    return render_template("login.html", token=generate_csrf())


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"success": "Logged out successfully"}), 200


@app.route("/profile")
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


@app.route("/signup", methods=["POST"])
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


@app.route("/signin", methods=["POST"])
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
