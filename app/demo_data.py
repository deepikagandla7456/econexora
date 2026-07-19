"""
Creates a fresh demo user with dummy stadium operations data every time someone clicks Preview Demo.
Old demo accounts older than 1 hour are cleaned up automatically.
"""
from datetime import datetime, date, timedelta, timezone
from werkzeug.security import generate_password_hash
import uuid


def create_demo_user():
    from app import db
    from app.models import User, OperationLog, Badge, Streak, GeneratedBroadcast, GeneratedDispatch

    # Clean up old demo accounts (older than 1 hour) using modern SQLAlchemy 2.0 select and delete syntax
    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=1)
    old_demos = db.session.scalars(
        db.select(User).filter_by(is_demo=True).filter(User.created_at < cutoff)
    ).all()

    for old in old_demos:
        db.session.execute(db.delete(OperationLog).filter_by(user_id=old.id))
        db.session.execute(db.delete(Badge).filter_by(user_id=old.id))
        db.session.execute(db.delete(Streak).filter_by(user_id=old.id))
        db.session.execute(db.delete(GeneratedBroadcast).filter_by(user_id=old.id))
        db.session.execute(db.delete(GeneratedDispatch).filter_by(user_id=old.id))
        db.session.delete(old)
    db.session.commit()

    # Create fresh demo user with unique ID
    uid = uuid.uuid4().hex[:8]
    demo_user = User(
        username=f"demo_{uid}",
        email=f"demo_{uid}@arenaops.demo",
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

    # Add demo stadium telemetry log entries
    demo_logs = [
        OperationLog(
            user_id=demo_user.id,
            title="Concourse A Spill reported",
            category="Logistics",
            severity="medium",
            location="Concourse A near Gate 2",
            actions_taken="Dispatched janitorial team with wet floor signs",
            resolution_progress=100,
            response_time=12.0,
            sensor_ref="https://stadiumops.live/sensors/spills/A2"
        ),
        OperationLog(
            user_id=demo_user.id,
            title="Gate 4 queue exceeds 25 min",
            category="Gates",
            severity="high",
            location="Gate 4 Entrance",
            actions_taken="Opened backup queue lanes and redirected fans to Gate 5",
            resolution_progress=100,
            response_time=15.0,
            sensor_ref="https://stadiumops.live/sensors/queues/gate4"
        ),
        OperationLog(
            user_id=demo_user.id,
            title="Parking Lot B capacity reached",
            category="Parking",
            severity="medium",
            location="Parking Lot B",
            actions_taken="Updated digital signage to direct traffic to Lot C",
            resolution_progress=100,
            response_time=8.0,
            sensor_ref="https://stadiumops.live/sensors/parking/lotb"
        ),
        OperationLog(
            user_id=demo_user.id,
            title="Power fluctuations in media box",
            category="Logistics",
            severity="medium",
            location="Media Center Box 4",
            actions_taken="Switched to backup generator and logged ticket with engineers",
            resolution_progress=100,
            response_time=25.0,
            sensor_ref="https://stadiumops.live/sensors/power/media"
        ),
        OperationLog(
            user_id=demo_user.id,
            title="Minor medical aid requested",
            category="Medical",
            severity="low",
            location="Sector 102 Row F",
            actions_taken="First aid dispatch treated minor knee scrape",
            resolution_progress=80,
            response_time=5.0,
            sensor_ref="https://stadiumops.live/alerts/medical/102F"
        ),
    ]
    for l in demo_logs:
        db.session.add(l)

    # Add demo badges
    demo_badges = [
        Badge(user_id=demo_user.id, name="First Dispatch", description="Generated your first emergency crew dispatch!", icon="🏆"),
        Badge(user_id=demo_user.id, name="Crisis Manager", description="Resolved 5 stadium operational incidents!", icon="🌿"),
    ]
    for b in demo_badges:
        db.session.add(b)

    # Add demo generated broadcast
    demo_broadcast = GeneratedBroadcast(
        user_id=demo_user.id,
        channel="public_alert",
        content="""Spectator Alert: Gate 4 is currently experiencing high wait times due to a scanner issue. Please proceed to Gate 3 or 5 for entry. Thank you for your patience! 🏟️"""
    )
    db.session.add(demo_broadcast)

    # Add demo generated dispatch
    demo_dispatch = GeneratedDispatch(
        user_id=demo_user.id,
        incident_title="Overcrowding at Gate 4",
        target_team="Security Crew A",
        dispatch_message="""Security Alert: Gate 4 wait times have exceeded 25 minutes. Security Crew A is requested to dispatch to Gate 4 immediately to assist with queue management and direct fans to Gate 5.""",
        followup_instructions="""Status check after 10 minutes. Ensure backup scanners are functional and report queue size updates."""
    )
    db.session.add(demo_dispatch)
    db.session.commit()

    return demo_user
