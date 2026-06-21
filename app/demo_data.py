"""
Creates a fresh demo user with dummy data every time someone clicks Preview Demo.
Old demo accounts older than 1 hour are cleaned up automatically.
"""
from datetime import datetime, date, timedelta, timezone
from werkzeug.security import generate_password_hash
import uuid


def create_demo_user():
    from app import db
    from app.models import User, Learning, Badge, Streak, GeneratedPost, GeneratedOutreach

    # Clean up old demo accounts (older than 1 hour)
    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=1)
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
        email=f"demo_{uid}@econexora.demo",
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

    # Add demo carbon tracker entries
    demo_learnings = [
        Learning(
            user_id=demo_user.id,
            title="Commuted via Electric Train",
            platform="Transport",
            resource_type="low",
            topic="0.8 kg CO2",
            skills="Electric Transit, Low-Carbon, Public Rail",
            progress=100,
            time_spent=25.0,
            url="https://ourworldindata.org/travel-carbon-footprint"
        ),
        Learning(
            user_id=demo_user.id,
            title="Red Meat (Beef Burger) Meal",
            platform="Food",
            resource_type="high",
            topic="6.2 kg CO2",
            skills="Red Meat, Food Emissions, High Impact",
            progress=100,
            time_spent=1.0,
            url="https://ourworldindata.org/environmental-impacts-of-food"
        ),
        Learning(
            user_id=demo_user.id,
            title="Run HVAC Air Conditioning (5 hours)",
            platform="Energy",
            resource_type="high",
            topic="3.5 kg CO2",
            skills="Grid Electricity, AC cooling, HVAC usage",
            progress=100,
            time_spent=5.0,
            url="https://www.eia.gov/energyexplained/use-of-energy/homes.php"
        ),
        Learning(
            user_id=demo_user.id,
            title="Plant-Based Vegan Lunch",
            platform="Food",
            resource_type="low",
            topic="0.4 kg CO2",
            skills="Plant-Based, Vegan diet, Low-carbon Meal",
            progress=100,
            time_spent=1.0,
            url="https://medium.com"
        ),
        Learning(
            user_id=demo_user.id,
            title="Home Solar Array Installation Check",
            platform="Energy",
            resource_type="low",
            topic="0.0 kg CO2",
            skills="Solar Power, Renewable Grid, Carbon Offset",
            progress=80,
            time_spent=2.0,
            url="https://nrel.gov"
        ),
    ]
    for l in demo_learnings:
        db.session.add(l)

    # Add demo badges
    demo_badges = [
        Badge(user_id=demo_user.id, name="First Post", description="Generated your first sustainability post!", icon="🏆"),
        Badge(user_id=demo_user.id, name="Eco Champion", description="Completed 5 offset goals!", icon="🌿"),
    ]
    for b in demo_badges:
        db.session.add(b)

    # Add demo generated post
    demo_post = GeneratedPost(
        user_id=demo_user.id,
        platform="linkedin",
        content="""Just completed a week of logging my carbon footprint with EcoNexora. 🌍

Honestly, the numbers are eye-opening. Transitioning to a plant-based lunch and taking the train instead of driving saved over 10kg of CO2 this week alone.

Key takeaways:
→ Transportation remains the largest source of my weekly personal carbon impact.
→ Diet choices (switching to vegan lunches) have a massive immediate emission reduction potential.
→ AC grid electric usage is highly dependent on fossil-fuel intensity.

Little changes accumulate to real environmental impact. What small habit are you changing to lower your personal emissions? 👇"""
    )
    db.session.add(demo_post)

    # Add demo outreach
    demo_outreach = GeneratedOutreach(
        user_id=demo_user.id,
        target_role="Carbon Management / ESG Intern",
        target_company="ClimatePartners",
        cold_dm="""Hi [Name],

I've been building tracking profiles mapping personal carbon footprint activities (transport, energy, food) using data from carbon accounting frameworks. I came across ClimatePartners' ESG tools and your focus on verified offset credits really resonates with me.

I'd love to learn more about the Carbon Management team and how you help enterprises audit their scope 1-3 emissions. Would you be open to a 10-minute chat?

Thanks!""",
        followup="""Hi [Name], just following up on my message. I know you're busy — would a quick 10-minute call work next week to discuss ESG analyst/intern roles at ClimatePartners? Happy to work around your schedule!"""
    )
    db.session.add(demo_outreach)
    db.session.commit()

    return demo_user
