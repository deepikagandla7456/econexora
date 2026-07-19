from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import OperationLog
from app.helpers import update_streak, check_and_award_badges

learning = Blueprint("learning", __name__)

CATEGORIES = ["Parking", "Gates", "Concessions", "Security", "Medical", "Logistics", "Other"]

SEVERITIES = ["low", "medium", "high", "critical"]


@learning.route("/learn", methods=["GET", "POST"])
@login_required
def learn():
    if request.method == "POST":
        if current_user.is_demo:
            flash("You're in demo mode — create a free account to save live stadium logs! 🏟️", "info")
            return redirect(url_for("learning.learn"))

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        severity = request.form.get("severity", "").strip()
        location = request.form.get("location", "").strip()
        actions_taken = request.form.get("actions_taken", "").strip()
        resolution_progress = request.form.get("resolution_progress", 0)
        response_time = request.form.get("response_time", 0)
        sensor_ref = request.form.get("sensor_ref", "").strip()

        if not title or not category or not location or not actions_taken:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("learning.learn"))

        try:
            resolution_progress = int(resolution_progress)
            response_time = float(response_time)
        except ValueError:
            flash("Progress and response time must be numeric values.", "error")
            return redirect(url_for("learning.learn"))

        entry = OperationLog(
            user_id=current_user.id,
            title=title,
            category=category,
            severity=severity or "low",
            location=location,
            actions_taken=actions_taken,
            resolution_progress=min(max(resolution_progress, 0), 100),
            response_time=max(response_time, 0),
            sensor_ref=sensor_ref if sensor_ref else None
        )
        db.session.add(entry)
        db.session.commit()

        update_streak(current_user)
        check_and_award_badges(current_user)

        flash("Incident logged and telemetry updated! 🏟️", "success")
        return redirect(url_for("learning.learn"))

    entries = OperationLog.query.filter_by(user_id=current_user.id).order_by(OperationLog.created_at.desc()).all()
    return render_template("learning.html", entries=entries, platforms=CATEGORIES, resource_types=SEVERITIES)


@learning.route("/learn/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    if current_user.is_demo:
        flash("You're in demo mode — create a free account to delete logs!", "info")
        return redirect(url_for("learning.learn"))
    entry = OperationLog.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash("Operational log deleted.", "info")
    return redirect(url_for("learning.learn"))


@learning.route("/learn/update/<int:entry_id>", methods=["POST"])
@login_required
def update_progress(entry_id):
    if current_user.is_demo:
        flash("You're in demo mode — create a free account to update resolution progress!", "info")
        return redirect(url_for("learning.learn"))
    entry = OperationLog.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if entry:
        try:
            progress = int(request.form.get("resolution_progress", entry.resolution_progress))
            entry.resolution_progress = min(max(progress, 0), 100)
            db.session.commit()
            check_and_award_badges(current_user)
            flash("Resolution progress updated!", "success")
        except ValueError:
            flash("Invalid progress value.", "error")
    return redirect(url_for("learning.learn"))
