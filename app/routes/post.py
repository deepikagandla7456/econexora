from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Learning, GeneratedPost
from app.helpers import build_skill_profile, generate_post, check_and_award_badges

post = Blueprint("post", __name__)


@post.route("/post", methods=["GET", "POST"])
@login_required
def generate():
    generated = None
    platform = None

    learnings = Learning.query.filter_by(user_id=current_user.id).all()

    if not learnings:
        flash("Add some learning entries first before generating a post!", "info")
        return render_template("post.html", generated=None, platform=None, past_posts=[])

    if request.method == "POST":
        if current_user.is_demo:
            flash("You're in demo mode — create a free account to generate your own AI posts! 🚀", "info")
            past_posts = GeneratedPost.query.filter_by(user_id=current_user.id).order_by(GeneratedPost.created_at.desc()).limit(5).all()
            return render_template("post.html", generated=None, platform=None, past_posts=past_posts)

        platform = request.form.get("platform", "linkedin")
        skill_profile = build_skill_profile(learnings)
        generated = generate_post(skill_profile, platform)

        if not generated.startswith("Error"):
            saved = GeneratedPost(user_id=current_user.id, platform=platform, content=generated)
            db.session.add(saved)
            db.session.commit()
            check_and_award_badges(current_user)

    past_posts = GeneratedPost.query.filter_by(user_id=current_user.id).order_by(GeneratedPost.created_at.desc()).limit(5).all()
    return render_template("post.html", generated=generated, platform=platform, past_posts=past_posts)
