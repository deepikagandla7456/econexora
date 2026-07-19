from app import db
from flask_login import UserMixin
from datetime import datetime, date, timezone


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_demo = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # Relationships
    operation_logs = db.relationship("OperationLog", backref="user", lazy=True)
    badges = db.relationship("Badge", backref="user", lazy=True)
    streak = db.relationship("Streak", backref="user", uselist=False, lazy=True)


class OperationLog(db.Model):
    __tablename__ = "operation_log"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)            # e.g., "High crowd wait time at Gate 3"
    category = db.Column(db.String(100), nullable=False)          # e.g., "Parking", "Gates", "Security"
    severity = db.Column(db.String(50), nullable=False)          # e.g., "low", "medium", "high", "critical"
    location = db.Column(db.String(200), nullable=False)          # e.g., "Gate 3 Entrance"
    actions_taken = db.Column(db.String(300), nullable=False)     # e.g., "Dispatched backup staff"
    resolution_progress = db.Column(db.Integer, default=0)        # 0 to 100%
    response_time = db.Column(db.Float, default=0)                # in minutes
    sensor_ref = db.Column(db.String(500), nullable=True)         # optional live link
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


class GeneratedBroadcast(db.Model):
    __tablename__ = "generated_broadcast"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    channel = db.Column(db.String(50), nullable=False)           # e.g., "public_alert", "staff_announcement"
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))


class GeneratedDispatch(db.Model):
    __tablename__ = "generated_dispatch"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    incident_title = db.Column(db.String(200), nullable=False)
    target_team = db.Column(db.String(200), nullable=False)       # e.g., "Security Team A", "Clean-up Crew"
    dispatch_message = db.Column(db.Text, nullable=False)
    followup_instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
