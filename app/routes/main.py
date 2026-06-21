from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Learning, Badge
from app.helpers import build_skill_profile, get_carbon_profile_data

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    all_learnings = Learning.query.filter_by(user_id=current_user.id).order_by(Learning.created_at.desc()).all()
    learnings = all_learnings[:5]
    badges = Badge.query.filter_by(user_id=current_user.id).all()
    streak = current_user.streak
    skill_profile = build_skill_profile(all_learnings)
    profile_data = get_carbon_profile_data(all_learnings)
    return render_template(
        "dashboard.html",
        learnings=learnings,
        badges=badges,
        streak=streak,
        skill_profile=skill_profile,
        profile_data=profile_data
    )
