"""
Creates a fresh demo user with dummy data every time someone clicks Preview Demo.
Old demo accounts older than 1 hour are cleaned up automatically.
"""
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash
import uuid


def create_demo_user():
    from app import db
    from app.models import User, Learning, Badge, Streak, GeneratedPost, GeneratedOutreach

    # Clean up old demo accounts (older than 1 hour)
    cutoff = datetime.utcnow() - timedelta(hours=1)
    old_demos = User.query.filter_by(is_demo=True).filter(User.created_at < cutoff).all()
    for old in old_demos:
        # Delete all related data first
        Learning.query.filter_by(user_id=old.id).delete()
        Badge.query.filter_by(user_id=old.id).delete()
        Streak.query.filter_by(user_id=old.id).delete()
        GeneratedPost.query.filter_by(user_id=old.id).delete()
        GeneratedOutreach.query.filter_by(user_id=old.id).delete()
        db.session.delete(old)
    db.session.commit()

    # Create fresh demo user with unique ID
    uid = uuid.uuid4().hex[:8]
    demo_user = User(
        username=f"demo_{uid}",
        email=f"demo_{uid}@skillnexora.demo",
        password=generate_password_hash("demo_pass"),
        is_demo=True
    )
    db.session.add(demo_user)
    db.session.commit()

    # Add demo streak
    streak = Streak(
        user_id=demo_user.id,
        current_streak=5,
        longest_streak=12,
        last_logged=date.today()
    )
    db.session.add(streak)

    # Add demo learning entries
    demo_learnings = [
        Learning(
            user_id=demo_user.id,
            title="Python for Data Science",
            platform="Coursera",
            resource_type="course",
            topic="Data Science",
            skills="Python, Pandas, NumPy, Matplotlib",
            progress=80,
            time_spent=12.0,
            url="https://coursera.org"
        ),
        Learning(
            user_id=demo_user.id,
            title="Flask Full Course",
            platform="YouTube",
            resource_type="video",
            topic="Web Development",
            skills="Flask, Python, HTML, CSS, SQLite",
            progress=100,
            time_spent=6.5,
            url="https://youtube.com"
        ),
        Learning(
            user_id=demo_user.id,
            title="Machine Learning A-Z",
            platform="Udemy",
            resource_type="course",
            topic="Machine Learning",
            skills="Scikit-learn, ML Algorithms, Feature Engineering",
            progress=55,
            time_spent=18.0,
            url="https://udemy.com"
        ),
        Learning(
            user_id=demo_user.id,
            title="DSA with Striver",
            platform="Takeuforward",
            resource_type="course",
            topic="Data Structures & Algorithms",
            skills="Arrays, Trees, Graphs, Dynamic Programming",
            progress=40,
            time_spent=20.0,
            url="https://takeuforward.org"
        ),
        Learning(
            user_id=demo_user.id,
            title="What is RAG? Explained Simply",
            platform="Medium",
            resource_type="blog",
            topic="Generative AI",
            skills="RAG, LLMs, Vector Databases, Embeddings",
            progress=100,
            time_spent=0.5,
            url="https://medium.com"
        ),
    ]
    for l in demo_learnings:
        db.session.add(l)

    # Add demo badges
    demo_badges = [
        Badge(user_id=demo_user.id, name="First Post", description="Generated your first social media post!", icon="🏆"),
        Badge(user_id=demo_user.id, name="First DM", description="Sent your first cold outreach!", icon="💼"),
    ]
    for b in demo_badges:
        db.session.add(b)

    # Add demo generated post
    demo_post = GeneratedPost(
        user_id=demo_user.id,
        platform="linkedin",
        content="""Just completed the Flask Full Course on YouTube — and honestly, it changed how I think about building things. 🚀

Started with zero backend knowledge. Now I've built a fully functional web app with login, database, and API integration.

Here's what clicked for me:
→ Flask is minimal by design — you only add what you need
→ SQLAlchemy makes databases feel like Python objects
→ Jinja2 templates are more powerful than I expected

The real learning was building something that actually works — not just following along.

If you're a frontend dev curious about backend, Flask is the gentlest entry point.

What framework did you start your backend journey with? 👇"""
    )
    db.session.add(demo_post)

    # Add demo outreach
    demo_outreach = GeneratedOutreach(
        user_id=demo_user.id,
        target_role="AI Engineer",
        target_company="Google",
        cold_dm="""Hi [Name],

I've been building AI-integrated web apps using Flask and Python, and recently completed projects involving LLMs and RAG systems. I came across your work at Google and the team's focus on responsible AI really resonates with me.

I'd love to learn more about the AI Engineer role and how the team approaches production ML. Would you be open to a 15-minute chat?

Thanks for your time!""",
        followup="""Hi [Name], just following up on my message from a few days ago. I know you're busy — would a quick 10-minute call work this week to discuss the AI Engineer role at Google? Happy to work around your schedule!"""
    )
    db.session.add(demo_outreach)
    db.session.commit()

    return demo_user
