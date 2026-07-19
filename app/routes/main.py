from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import OperationLog, Badge
from app.helpers import build_skill_profile, get_operations_profile_data

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    # Efficient: Limit log fetch to recent 5 entries in database
    recent_logs = db.session.scalars(
        db.select(OperationLog)
        .filter_by(user_id=current_user.id)
        .order_by(OperationLog.created_at.desc())
        .limit(5)
    ).all()

    # Modern select syntax
    badges = db.session.scalars(
        db.select(Badge).filter_by(user_id=current_user.id)
    ).all()

    streak = current_user.streak
    
    # Highly efficient DB-level stats aggregation instead of loading all log objects
    skill_profile = build_skill_profile(current_user.id)
    profile_data = get_operations_profile_data(current_user.id)

    return render_template(
        "dashboard.html",
        learnings=recent_logs,
        badges=badges,
        streak=streak,
        skill_profile=skill_profile,
        profile_data=profile_data
    )
