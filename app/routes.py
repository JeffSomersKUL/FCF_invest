from app import app, db
import os
from flask import jsonify, render_template, request, redirect, url_for
from flask import send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from app.models import ContactFormData
from sqlalchemy.exc import SQLAlchemyError

class ContactForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Email Content', validators=[DataRequired()])

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

@app.route('/submit_form', methods=['POST'])
def submit_form():
    form = ContactForm(request.form)

    if form.validate():
        # Form data is valid
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        subject = form.subject.data
        content = form.content.data

        print(f"Form received! First Name: {fname},  Last Name: {lname}, Email: {email}, Subject: {subject}, Content: {content}")

        form_data = ContactFormData(fname=fname, lname=lname, email=email, subject=subject, content=content)

        try:
            # Attempt to add the data to the session and commit to the database
            db.session.add(form_data)
            db.session.commit()
            return{"response": "success"}
        except SQLAlchemyError as e:
            # Handle the specific exception (e.g., IntegrityError)
            db.session.rollback()  # Rollback the transaction to avoid leaving the database in an inconsistent state
            return {"response": "failed"}
    else:

        return{"response": list(form.errors.keys())}
    

@app.route("/cc7fccf50f9946b1e93dcc29946b13ef")
def view_messages():
    # Query all messages from the database
    messages = ContactFormData.query.all()

    return render_template('messages.html', messages=messages)

@app.route('/delete_message/<int:message_id>')
def delete_message(message_id):
    message = ContactFormData.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
    return redirect(url_for('view_messages'))

