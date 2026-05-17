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


def build_skill_profile(learnings):
    """Build a text summary of user's skills from their learning entries."""
    if not learnings:
        return "No learning entries yet."

    skills_set = set()
    topics = []
    platforms = []
    total_hours = 0

    for l in learnings:
        for s in l.skills.split(","):
            skills_set.add(s.strip())
        topics.append(l.topic)
        platforms.append(l.platform)
        total_hours += l.time_spent or 0

    profile = f"""
Skills: {', '.join(skills_set)}
Topics studied: {', '.join(set(topics))}
Platforms used: {', '.join(set(platforms))}
Total learning hours: {round(total_hours, 1)}
Number of resources: {len(learnings)}
    """.strip()

    return profile


def generate_post(skill_profile, platform):
    """Generate a LinkedIn or Twitter post using Groq."""
    if not get_groq_client():
        return "Error: GROQ_API_KEY not set. Please add it to your .env file."

    if platform == "linkedin":
        prompt = f"""
You are a career coach helping a student write a LinkedIn post about their recent learning journey.

Based on this skill profile:
{skill_profile}

Write a professional LinkedIn post that:
- Starts with a hook (not "I am excited to share")
- Tells a short story about what they learned
- Mentions 2-3 specific skills
- Ends with a takeaway or question for readers
- Uses line breaks for readability
- Is 150-200 words max
- Sounds human and natural, not AI-generated

Only return the post text. No explanation.
"""
    else:
        prompt = f"""
You are helping a student write a Twitter/X thread about their learning.

Based on this skill profile:
{skill_profile}

Write a punchy Twitter thread (3-4 tweets) that:
- Tweet 1: Strong hook about what they learned
- Tweet 2: Key insight or skill breakdown
- Tweet 3: Practical takeaway
- Tweet 4 (optional): Call to action
- Each tweet under 280 characters
- Label them as 1/, 2/, 3/ etc

Only return the thread text. No explanation.
"""

    try:
        result = groq_chat(prompt)
        if result is None:
            return "Error: GROQ_API_KEY not set."
        return result
    except Exception as e:
        return f"Error generating post: {str(e)}"


def generate_outreach(skill_profile, target_role, target_company):
    """Generate cold DM and follow-up message using Groq."""
    if not get_groq_client():
        return (
            "Error: GROQ_API_KEY not set. Please add it to your .env file.",
            "Error: GROQ_API_KEY not set. Please add it to your .env file."
        )

    cold_prompt = f"""
Write a short, personalized cold LinkedIn DM from a student to a hiring manager at {target_company} for the role of {target_role}.

The student's skill profile:
{skill_profile}

Rules:
- Max 100 words
- Mention 1-2 specific skills from the profile that match the role
- Sound human and genuine, not copy-paste
- End with a soft ask (a call or quick chat)
- No subject line needed

Only return the DM text.
"""

    followup_prompt = f"""
Write a short follow-up LinkedIn DM to send 4 days after the first message to a hiring manager at {target_company} for the role of {target_role}.

Rules:
- Max 60 words
- Reference that you sent a message earlier
- Stay polite and not pushy
- Restate 1 skill briefly
- End with an easy yes/no question

Only return the follow-up DM text.
"""

    try:
        cold = groq_chat(cold_prompt)
        followup = groq_chat(followup_prompt)
        if cold is None or followup is None:
            return ("Error: GROQ_API_KEY not set.", "Error: GROQ_API_KEY not set.")
        return cold, followup
    except Exception as e:
        err = f"Error: {str(e)}"
        return err, err


def update_streak(user):
    """Update the user's streak based on today's date."""
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
        return  # already logged today

    if streak.last_logged == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1  # streak broken, reset

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.last_logged = today
    db.session.commit()


def check_and_award_badges(user):
    """Check conditions and award badges the user hasn't earned yet."""
    from app import db
    from app.models import Badge, Learning, GeneratedPost, GeneratedOutreach

    existing = {b.name for b in user.badges}

    def award(name, description, icon):
        if name not in existing:
            badge = Badge(user_id=user.id, name=name, description=description, icon=icon)
            db.session.add(badge)
            existing.add(name)

    # Badge: 7-day streak
    if user.streak and user.streak.current_streak >= 7:
        award("7-Day Streak", "Logged learning 7 days in a row!", "🔥")

    # Badge: 5 courses completed
    completed = Learning.query.filter_by(user_id=user.id).filter(Learning.progress == 100).count()
    if completed >= 5:
        award("Course Champion", "Completed 5 courses!", "📚")

    # Badge: First post generated
    posts = GeneratedPost.query.filter_by(user_id=user.id).count()
    if posts >= 1:
        award("First Post", "Generated your first social media post!", "🏆")

    # Badge: First cold DM sent
    dms = GeneratedOutreach.query.filter_by(user_id=user.id).count()
    if dms >= 1:
        award("First DM", "Sent your first cold outreach!", "💼")

    db.session.commit()
