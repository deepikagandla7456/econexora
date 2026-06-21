from app import db
from flask_login import UserMixin
from datetime import datetime, date, timezone


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_demo = db.Column(db.Boolean, default=False)   # NEW: marks demo accounts
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    learnings = db.relationship("Learning", backref="user", lazy=True)
    badges = db.relationship("Badge", backref="user", lazy=True)
    streak = db.relationship("Streak", backref="user", uselist=False, lazy=True)


class Learning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    skills = db.Column(db.String(300), nullable=False)
    progress = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Float, default=0)
    url = db.Column(db.String(500), nullable=True)
    logged_date = db.Column(db.Date, default=date.today, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(10), nullable=False)
    earned_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))


class Streak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_logged = db.Column(db.Date, nullable=True)


class GeneratedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    platform = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))


class GeneratedOutreach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    target_role = db.Column(db.String(200), nullable=False)
    target_company = db.Column(db.String(200), nullable=False)
    cold_dm = db.Column(db.Text, nullable=False)
    followup = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
