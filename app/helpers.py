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
    """Build a summary of user's carbon footprint from their logs."""
    if not learnings:
        return "No carbon tracking entries yet."

    impact_tags = set()
    categories = []
    total_quantity = 0
    total_emissions = 0.0

    for l in learnings:
        for s in l.skills.split(","):
            impact_tags.add(s.strip())
        categories.append(l.platform)
        total_quantity += l.time_spent or 0
        try:
            # Extract numerical emission value, e.g., "4.5 kg CO2" -> 4.5
            val = float(l.topic.replace("kg CO2", "").replace("kg", "").strip())
            total_emissions += val
        except ValueError:
            pass

    profile = f"""
Eco Impact Tags: {', '.join(impact_tags)}
Categories Logged: {', '.join(set(categories))}
Total Activity Log Hours/Km: {round(total_quantity, 1)}
Total CO2 Emissions: {round(total_emissions, 1)} kg CO2
Number of Logs: {len(learnings)}
    """.strip()

    return profile


def generate_post(skill_profile, platform):
    """Generate a LinkedIn or Twitter/X post showing carbon footprint awareness using Groq."""
    if not get_groq_client():
        return "Error: GROQ_API_KEY not set. Please add it to your .env file."

    if platform == "linkedin":
        prompt = f"""
You are a sustainability advocate helping an individual write a LinkedIn post about their carbon footprint tracking journey.

Based on this carbon footprint profile:
{skill_profile}

Write a professional LinkedIn post that:
- Starts with a hook about personal climate action
- Shares a short insight on what they tracked (e.g. transport, meals, home energy)
- Mentions 2-3 specific eco impact tags and the total CO2 emissions
- Ends with an encouraging takeaway or question for others to reduce their emissions
- Uses line breaks for readability
- Is 150-200 words max
- Sounds human and natural, not AI-generated

Only return the post text. No explanation.
"""
    else:
        prompt = f"""
You are helping a green advocate write a Twitter/X thread (3-4 tweets) about their carbon footprint tracking.

Based on this profile:
{skill_profile}

Write a punchy Twitter thread that:
- Tweet 1: Strong hook about tracking carbon emissions
- Tweet 2: Key insight or emission reduction tip
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
    """Generate cold DM to sustainability manager or green company using Groq."""
    if not get_groq_client():
        return (
            "Error: GROQ_API_KEY not set. Please add it to your .env file.",
            "Error: GROQ_API_KEY not set. Please add it to your .env file."
        )

    cold_prompt = f"""
Write a short, personalized cold LinkedIn DM from a green advocate to a Sustainability Manager or ESG Lead at {target_company} for the role/initiative of {target_role}.

The sender's carbon profile details:
{skill_profile}

Rules:
- Max 100 words
- Mention their carbon tracking efforts or eco impact tags
- Sound human and genuine
- End with a soft ask (a quick virtual chat about their carbon management initiatives)
- No subject line needed

Only return the DM text.
"""

    followup_prompt = f"""
Write a short follow-up LinkedIn DM to send 4 days after the first message to the Sustainability Lead at {target_company} for the role/initiative of {target_role}.

Rules:
- Max 60 words
- Reference that you sent a message earlier
- Stay polite and not pushy
- Restate interest in carbon reduction briefly
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
        award("7-Day Streak", "Logged carbon footprint activities 7 days in a row!", "🔥")

    # Badge: 5 offset goals completed
    completed = Learning.query.filter_by(user_id=user.id).filter(Learning.progress == 100).count()
    if completed >= 5:
        award("Eco Champion", "Completed 5 offset goals!", "🌿")

    # Badge: First post generated
    posts = GeneratedPost.query.filter_by(user_id=user.id).count()
    if posts >= 1:
        award("First Post", "Generated your first sustainability post!", "🏆")

    # Badge: First cold DM sent
    dms = GeneratedOutreach.query.filter_by(user_id=user.id).count()
    if dms >= 1:
        award("First DM", "Generated your first climate outreach DM!", "💼")

    db.session.commit()
