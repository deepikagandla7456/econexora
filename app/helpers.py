import os
from datetime import date, timedelta


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    from groq import Groq
    return Groq(api_key=api_key)


def groq_chat(prompt):
    """Send a prompt to Groq and return the response text."""
    client = get_groq_client()
    if not client:
        return None
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()


def build_skill_profile(operation_logs):
    """Build a summary of stadium operations status from the logs."""
    if not operation_logs:
        return "No stadium operational incidents logged yet."

    categories = set()
    severities = set()
    total_response_time = 0.0
    resolved_count = 0

    for l in operation_logs:
        if l.category:
            categories.add(l.category)
        if l.severity:
            severities.add(l.severity)
        total_response_time += float(l.response_time or 0)
        if l.resolution_progress == 100:
            resolved_count += 1

    profile = f"""
Stadium Operational Categories: {', '.join(sorted(list(categories)))}
Severities Addressed: {', '.join(sorted(list(severities)))}
Total Incident Logged: {len(operation_logs)}
Resolved Incidents: {resolved_count}
Average Operator Response Time: {round(total_response_time / len(operation_logs), 1) if operation_logs else 0} mins
    """.strip()

    return profile


def get_operations_profile_data(operation_logs):
    """Build a structured dict of stadium operations stats for rendering in UI."""
    if not operation_logs:
        return {
            "categories": [],
            "severities": [],
            "total_response_time": 0.0,
            "average_response_time": 0.0,
            "resolved_count": 0,
            "count": 0
        }
    
    categories = set()
    severities = set()
    total_response_time = 0.0
    resolved_count = 0

    for l in operation_logs:
        if l.category:
            categories.add(l.category)
        if l.severity:
            severities.add(l.severity)
        total_response_time += float(l.response_time or 0)
        if l.resolution_progress == 100:
            resolved_count += 1
                
    return {
        "categories": sorted(list(categories)),
        "severities": sorted(list(severities)),
        "total_response_time": round(total_response_time, 1),
        "average_response_time": round(total_response_time / len(operation_logs), 1) if operation_logs else 0.0,
        "resolved_count": resolved_count,
        "count": len(operation_logs)
    }


def generate_post(ops_profile, channel):
    """Generate official public PR stadium announcements or internal staff alerts using Groq."""
    if not get_groq_client():
        return "Error: GROQ_API_KEY not set. Please add it to your .env file."

    if channel == "public_alert":
        prompt = f"""
You are the Public Relations Lead for a smart sports stadium.
Based on the current stadium operations telemetry profile:
{ops_profile}

Write a professional, clear public announcement for fans and spectators that:
- Starts with a spectator safety and operations update
- Highlights dynamic crowd flow directions (e.g. queue redirection, parking status)
- Gives constructive advice to minimize travel delay (using 2-3 specific locations/categories)
- Ends with an encouraging, welcoming sports-themed closing
- Uses line breaks for clean readability
- Is under 150 words max
- Sounds natural, calm, and professional, not AI-generated

Only return the broadcast announcement text. No explanations.
"""
    else:
        prompt = f"""
You are the Operations Director of a smart stadium tournament.
Based on this operational profile:
{ops_profile}

Write a concise staff notification message (WhatsApp/SMS style, 3-4 bullet items) that:
- Summarizes incident resolutions and outstanding items
- Mentions immediate response protocols for critical/high severity zones
- Sets clear expectations for the upcoming match shift
- Keeps the tone direct, professional, and urgent
- Under 250 characters total

Only return the notification text. No explanations.
"""

    try:
        result = groq_chat(prompt)
        if result is None:
            return "Error: GROQ_API_KEY not set."
        return result
    except Exception as e:
        return f"Error generating announcement: {str(e)}"


def generate_outreach(ops_profile, incident_title, target_team):
    """Generate SMS/WhatsApp dispatch crew alerts using Groq."""
    if not get_groq_client():
        return (
            "Error: GROQ_API_KEY not set. Please add it to your .env file.",
            "Error: GROQ_API_KEY not set. Please add it to your .env file."
        )

    dispatch_prompt = f"""
Write a short, highly-urgent SMS dispatch alert to the {target_team} regarding the stadium incident: "{incident_title}".

Use this stadium operations profile for context:
{ops_profile}

Rules:
- Max 100 words
- State the incident, location, severity, and immediate instructions for {target_team}
- End with a request to confirm dispatch (e.g., 'Reply ACK to confirm')
- Keep it highly professional, clear, and urgent

Only return the dispatch message text.
"""

    followup_prompt = f"""
Write a short follow-up SMS check-in message to send to {target_team} 10 minutes after dispatch for "{incident_title}".

Rules:
- Max 60 words
- Reference the previous incident alert
- Ask for immediate resolution status or roadblock updates
- Tone must be concise, helpful, and direct

Only return the follow-up text.
"""

    try:
        cold = groq_chat(dispatch_prompt)
        followup = groq_chat(followup_prompt)
        if cold is None or followup is None:
            return ("Error: GROQ_API_KEY not set.", "Error: GROQ_API_KEY not set.")
        return cold, followup
    except Exception as e:
        err = f"Error: {str(e)}"
        return err, err


def update_streak(user):
    """Update the user's logging streak based on today's date."""
    from app import db
    from app.models import Streak

    today = date.today()

    if not user.streak:
        streak = Streak(user_id=user.id, current_streak=1, longest_streak=1, last_logged=today)
        db.session.add(streak)
        db.session.commit()
        return

    streak = user.streak

    if streak.last_logged == today:
        return

    if streak.last_logged == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.last_logged = today
    db.session.commit()


def check_and_award_badges(user):
    """Check conditions and award operations badges."""
    from app import db
    from app.models import Badge, OperationLog, GeneratedBroadcast, GeneratedDispatch

    existing = {b.name for b in user.badges}

    def award(name, description, icon):
        if name not in existing:
            badge = Badge(user_id=user.id, name=name, description=description, icon=icon)
            db.session.add(badge)
            existing.add(name)

    # Badge: 7-day streak
    if "7-Day Streak" not in existing:
        if user.streak and user.streak.current_streak >= 7:
            award("7-Day Streak", "Logged operational logs 7 days in a row!", "🔥")

    # Badge: Crisis Manager (5 resolved incidents)
    if "Crisis Manager" not in existing:
        completed = OperationLog.query.filter_by(user_id=user.id).filter(OperationLog.resolution_progress == 100).count()
        if completed >= 5:
            award("Crisis Manager", "Resolved 5 stadium operational incidents!", "🌿")

    # Badge: First Broadcast
    if "First Broadcast" not in existing:
        broadcasts = GeneratedBroadcast.query.filter_by(user_id=user.id).count()
        if broadcasts >= 1:
            award("First Broadcast", "Generated your first fan broadcast alert!", "🏆")

    # Badge: First Dispatch
    if "First Dispatch" not in existing:
        dispatches = GeneratedDispatch.query.filter_by(user_id=user.id).count()
        if dispatches >= 1:
            award("First Dispatch", "Generated your first emergency crew dispatch!", "💼")

    db.session.commit()
