from app import db
from datetime import datetime, timezone


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
