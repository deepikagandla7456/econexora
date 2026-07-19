from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import OperationLog, GeneratedDispatch
from app.helpers import build_skill_profile, generate_outreach, check_and_award_badges

outreach = Blueprint("outreach", __name__)


@outreach.route("/outreach", methods=["GET", "POST"])
@login_required
def cold_outreach():
    cold_dm = None
    followup = None

    # Efficient: count incidents in DB instead of pulling full logs objects list
    count = db.session.scalar(
        db.select(db.func.count(OperationLog.id)).filter_by(user_id=current_user.id)
    ) or 0

    if count == 0:
        flash("Log some operational events first before dispatching alert DMs!", "info")
        return render_template("outreach.html", cold_dm=None, followup=None, past=[])

    if request.method == "POST":
        if current_user.is_demo:
            flash("You're in demo mode — create a free account to trigger AI staff dispatch alerts! 🚀", "info")
            # Modern select query
            past = db.session.scalars(
                db.select(GeneratedDispatch)
                .filter_by(user_id=current_user.id)
                .order_by(GeneratedDispatch.created_at.desc())
                .limit(5)
            ).all()
            return render_template("outreach.html", cold_dm=None, followup=None, past=past)

        incident_title = request.form.get("target_role", "").strip()
        target_team = request.form.get("target_company", "").strip()

        if not incident_title or not target_team:
            flash("Please enter both incident title and target crew team.", "error")
            return render_template("outreach.html", cold_dm=None, followup=None, past=[])

        # Efficient DB aggregate summary
        ops_profile = build_skill_profile(current_user.id)
        cold_dm, followup = generate_outreach(ops_profile, incident_title, target_team)

        if not cold_dm.startswith("Error"):
            saved = GeneratedDispatch(
                user_id=current_user.id,
                incident_title=incident_title,
                target_team=target_team,
                dispatch_message=cold_dm,
                followup_instructions=followup
            )
            db.session.add(saved)
            db.session.commit()
            check_and_award_badges(current_user)

    # Modern select query
    past = db.session.scalars(
        db.select(GeneratedDispatch)
        .filter_by(user_id=current_user.id)
        .order_by(GeneratedDispatch.created_at.desc())
        .limit(5)
    ).all()
    return render_template("outreach.html", cold_dm=cold_dm, followup=followup, past=past)
