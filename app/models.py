from app import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string


class ContactFormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc)
    )


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    current = db.Column(db.Boolean, default=True)

    # Define a relationship with the User model
    user = db.relationship(
        "User",
        back_populates="member",
        uselist=False,
        cascade="all, delete-orphan",
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    confirmed = db.Column(db.Boolean, default=False)
    confirmation_code = db.Column(db.String(6), nullable=True)

    # Foreign key linking to the Member model
    member_id = db.Column(
        db.Integer, db.ForeignKey("member.id"), nullable=False
    )

    # Define a relationship with the Member model
    member = db.relationship("Member", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_code(self):
        self.confirmation_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))
