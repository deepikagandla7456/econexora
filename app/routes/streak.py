from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Badge, OperationLog

streak = Blueprint("streak", __name__)

ALL_BADGES = [
    {"name": "7-Day Streak", "icon": "🔥", "description": "Logged operational logs 7 days in a row!"},
    {"name": "Crisis Manager", "icon": "🌿", "description": "Resolved 5 stadium operational incidents!"},
    {"name": "First Broadcast", "icon": "🏆", "description": "Generated your first fan broadcast alert!"},
    {"name": "First Dispatch", "icon": "💼", "description": "Generated your first emergency crew dispatch!"},
]


@streak.route("/streak")
@login_required
def streak_page():
    # Modern select query
    user_badges = db.session.scalars(
        db.select(Badge).filter_by(user_id=current_user.id)
    ).all()
    earned_names = {b.name for b in user_badges}

    # Mark which badges are earned vs locked
    badge_status = []
    for b in ALL_BADGES:
        badge_status.append({
            "name": b["name"],
            "icon": b["icon"],
            "description": b["description"],
            "earned": b["name"] in earned_names
        })

    streak_data = current_user.streak
    
    # Highly efficient DB-level counting instead of loading full logs list in memory
    total_entries = db.session.scalar(
        db.select(db.func.count(OperationLog.id)).filter_by(user_id=current_user.id)
    ) or 0
    
    completed = db.session.scalar(
        db.select(db.func.count(OperationLog.id))
        .filter_by(user_id=current_user.id)
        .filter(OperationLog.resolution_progress == 100)
    ) or 0

    return render_template(
        "streak.html",
        streak=streak_data,
        badge_status=badge_status,
        user_badges=user_badges,
        total_entries=total_entries,
        completed=completed
    )
