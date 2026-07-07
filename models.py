from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    dob = db.Column(
        db.Date,
        nullable=False
    )

    token = db.Column(
        db.String(100),
        unique=True,
        default=lambda: str(uuid.uuid4())
    )

    register_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    last_mail_sent = db.Column(
        db.Date,
        nullable=True
    )

    next_mail_date = db.Column(
        db.Date,
        nullable=True
    )