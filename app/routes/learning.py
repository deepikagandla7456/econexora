from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Learning
from app.helpers import update_streak, check_and_award_badges

learning = Blueprint("learning", __name__)

PLATFORMS = ["Transport", "Food", "Energy", "Waste", "Water", "Shopping", "Other"]

RESOURCE_TYPES = ["low", "medium", "high", "offset", "other"]


@learning.route("/learn", methods=["GET", "POST"])
@login_required
def learn():
    if request.method == "POST":
        if current_user.is_demo:
            flash("You're in demo mode — create a free account to save your eco-activities! 🌿", "info")
            return redirect(url_for("learning.learn"))

        title = request.form.get("title", "").strip()
        platform = request.form.get("platform", "").strip()
        resource_type = request.form.get("resource_type", "").strip()
        topic = request.form.get("topic", "").strip()
        skills = request.form.get("skills", "").strip()
        progress = request.form.get("progress", 0)
        time_spent = request.form.get("time_spent", 0)
        url = request.form.get("url", "").strip()

        if not title or not platform or not topic or not skills:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("learning.learn"))

        try:
            progress = int(progress)
            time_spent = float(time_spent)
        except ValueError:
            progress = 0
            time_spent = 0

        entry = Learning(
            user_id=current_user.id,
            title=title,
            platform=platform,
            resource_type=resource_type or "other",
            topic=topic,
            skills=skills,
            progress=min(max(progress, 0), 100),
            time_spent=max(time_spent, 0),
            url=url if url else None
        )
        db.session.add(entry)
        db.session.commit()

        update_streak(current_user)
        check_and_award_badges(current_user)

        flash("Eco-activity logged! Keep up the green habits 🌿", "success")
        return redirect(url_for("learning.learn"))

    entries = Learning.query.filter_by(user_id=current_user.id).order_by(Learning.created_at.desc()).all()
    return render_template("learning.html", entries=entries, platforms=PLATFORMS, resource_types=RESOURCE_TYPES)


@learning.route("/learn/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    if current_user.is_demo:
        flash("You're in demo mode — create a free account to manage your entries!", "info")
        return redirect(url_for("learning.learn"))
    entry = Learning.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash("Entry deleted.", "info")
    return redirect(url_for("learning.learn"))


@learning.route("/learn/update/<int:entry_id>", methods=["POST"])
@login_required
def update_progress(entry_id):
    if current_user.is_demo:
        flash("You're in demo mode — create a free account to update progress!", "info")
        return redirect(url_for("learning.learn"))
    entry = Learning.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if entry:
        try:
            progress = int(request.form.get("progress", entry.progress))
            entry.progress = min(max(progress, 0), 100)
            db.session.commit()
            check_and_award_badges(current_user)
            flash("Progress updated!", "success")
        except ValueError:
            flash("Invalid progress value.", "error")
    return redirect(url_for("learning.learn"))
