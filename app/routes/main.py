from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
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
    all_logs = OperationLog.query.filter_by(user_id=current_user.id).order_by(OperationLog.created_at.desc()).all()
    recent_logs = all_logs[:5]
    badges = Badge.query.filter_by(user_id=current_user.id).all()
    streak = current_user.streak
    skill_profile = build_skill_profile(all_logs)
    profile_data = get_operations_profile_data(all_logs)
    return render_template(
        "dashboard.html",
        learnings=recent_logs,
        badges=badges,
        streak=streak,
        skill_profile=skill_profile,
        profile_data=profile_data
    )
