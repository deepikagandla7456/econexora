from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Badge, Learning

streak = Blueprint("streak", __name__)

ALL_BADGES = [
    {"name": "7-Day Streak", "icon": "🔥", "description": "Logged carbon footprint activities 7 days in a row!"},
    {"name": "Eco Champion", "icon": "🌿", "description": "Completed 5 offset goals!"},
    {"name": "First Post", "icon": "🏆", "description": "Generated your first sustainability post!"},
    {"name": "First DM", "icon": "💼", "description": "Generated your first climate outreach DM!"},
]


@streak.route("/streak")
@login_required
def streak_page():
    user_badges = Badge.query.filter_by(user_id=current_user.id).all()
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
    learnings = Learning.query.filter_by(user_id=current_user.id).all()
    total_entries = len(learnings)
    completed = sum(1 for l in learnings if l.progress == 100)

    return render_template(
        "streak.html",
        streak=streak_data,
        badge_status=badge_status,
        user_badges=user_badges,
        total_entries=total_entries,
        completed=completed
    )
