from flask import render_template, request
from sqlalchemy.exc import SQLAlchemyError

from . import main
from app import db
from .models import ContactFormData
from .forms import ContactForm


@main.route("/")
def index():
    form = ContactForm(request.form)
    return render_template("home.html", form=form)


@main.route("/about/leadership")
def leadership():
    return render_template("leadership.html")


@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/submit_form", methods=["POST"])
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
