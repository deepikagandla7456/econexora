from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import OperationLog, GeneratedBroadcast
from app.helpers import build_skill_profile, generate_post, check_and_award_badges

post = Blueprint("post", __name__)


@post.route("/post", methods=["GET", "POST"])
@login_required
def generate():
    generated = None
    platform = None

    # Efficient: count incidents in DB instead of pulling full logs objects list
    count = db.session.scalar(
        db.select(db.func.count(OperationLog.id)).filter_by(user_id=current_user.id)
    ) or 0

    if count == 0:
        flash("Log some operational events first before generating broadcasts!", "info")
        return render_template("post.html", generated=None, platform=None, past_posts=[])

    if request.method == "POST":
        if current_user.is_demo:
            flash("You're in demo mode — create a free account to generate AI broadcasts! 🚀", "info")
            # Modern select query
            past_posts = db.session.scalars(
                db.select(GeneratedBroadcast)
                .filter_by(user_id=current_user.id)
                .order_by(GeneratedBroadcast.created_at.desc())
                .limit(5)
            ).all()
            return render_template("post.html", generated=None, platform=None, past_posts=past_posts)

        platform = request.form.get("platform", "public_alert")
        # Efficient DB aggregate summary
        ops_profile = build_skill_profile(current_user.id)
        generated = generate_post(ops_profile, platform)

        if not generated.startswith("Error"):
            saved = GeneratedBroadcast(user_id=current_user.id, channel=platform, content=generated)
            db.session.add(saved)
            db.session.commit()
            check_and_award_badges(current_user)

    # Modern select query
    past_posts = db.session.scalars(
        db.select(GeneratedBroadcast)
        .filter_by(user_id=current_user.id)
        .order_by(GeneratedBroadcast.created_at.desc())
        .limit(5)
    ).all()
    return render_template("post.html", generated=generated, platform=platform, past_posts=past_posts)
