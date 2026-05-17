from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Learning, GeneratedOutreach
from app.helpers import build_skill_profile, generate_outreach, check_and_award_badges

outreach = Blueprint("outreach", __name__)


@outreach.route("/outreach", methods=["GET", "POST"])
@login_required
def cold_outreach():
    cold_dm = None
    followup = None

    learnings = Learning.query.filter_by(user_id=current_user.id).all()

    if not learnings:
        flash("Add some learning entries first so we can personalize your outreach!", "info")
        return render_template("outreach.html", cold_dm=None, followup=None, past=[])

    if request.method == "POST":
        if current_user.is_demo:
            flash("You're in demo mode — create a free account to generate personalized outreach! 🚀", "info")
            past = GeneratedOutreach.query.filter_by(user_id=current_user.id).order_by(GeneratedOutreach.created_at.desc()).limit(5).all()
            return render_template("outreach.html", cold_dm=None, followup=None, past=past)

        target_role = request.form.get("target_role", "").strip()
        target_company = request.form.get("target_company", "").strip()

        if not target_role or not target_company:
            flash("Please enter both target role and company.", "error")
            return render_template("outreach.html", cold_dm=None, followup=None, past=[])

        skill_profile = build_skill_profile(learnings)
        cold_dm, followup = generate_outreach(skill_profile, target_role, target_company)

        if not cold_dm.startswith("Error"):
            saved = GeneratedOutreach(
                user_id=current_user.id,
                target_role=target_role,
                target_company=target_company,
                cold_dm=cold_dm,
                followup=followup
            )
            db.session.add(saved)
            db.session.commit()
            check_and_award_badges(current_user)

    past = GeneratedOutreach.query.filter_by(user_id=current_user.id).order_by(GeneratedOutreach.created_at.desc()).limit(5).all()
    return render_template("outreach.html", cold_dm=cold_dm, followup=followup, past=past)
