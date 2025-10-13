import random
import string
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login_manager


class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    current = db.Column(db.Boolean, default=True)

    # Define relationships
    user = db.relationship(
        "User",
        back_populates="member",
        uselist=False,
        cascade="all, delete-orphan",
    )
    transfers = db.relationship(
        "MemberTransfer",
        back_populates="member",
        cascade="all, delete-orphan",
    )
    investments = db.relationship(
        "MemberInvestment",
        back_populates="member",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"{self.fname} {self.lname}"


class MemberTransfer(db.Model):
    __tablename__ = "member_transfer"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey("member.id"), nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    # Define relationships
    member = db.relationship("Member", back_populates="transfers")

    def __repr__(self):
        return f"<MemberTransfer {self.member.name} {self.amount}>"


class MemberInvestment(db.Model):
    __tablename__ = "member_investment"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey("member.id"), nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    stocks_received = db.Column(db.Integer, nullable=False)
    information = db.Column(db.Text, nullable=True)

    # Define relationships
    member = db.relationship("Member", back_populates="investments")

    def __repr__(self):
        return f"<Investment €{self.amount} for {self.stocks_received} on {self.date}>"


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey("member.id"), nullable=False
    )
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    confirmed = db.Column(db.Boolean, default=False)
    confirmation_code = db.Column(db.String(6), nullable=True)

    # Define relationships
    member = db.relationship("Member", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_code(self):
        self.confirmation_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    def __repr__(self):
        return self.email


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))
