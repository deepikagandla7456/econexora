# SkillNexora 🚀

> Track your learning. Generate posts. Get noticed.

SkillNexora helps students and job seekers turn their daily learning into LinkedIn posts, cold outreach messages, and a portfolio — all powered by AI.

---

## Features

| Feature | What it does |
|---|---|
| 📚 Learning Tracker | Log courses, videos, blogs and track progress |
| ✍️ Post Generator | AI writes LinkedIn & Twitter posts from your learning |
| 📩 Cold Outreach | Personalized cold DMs to hiring managers |
| 🔥 Streak & Badges | Daily streaks and milestone badges |

---

## Tech Stack

| Part | Tool |
|---|---|
| Backend | Python + Flask |
| AI | Gemini API |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/deepikagandla7456/skillnexora.git
cd skillnexora
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your GROQ API key**

Copy `.env.example` to `.env` and fill in:
```
GROQ_API_KEY=your_key_here
SECRET_KEY=any_random_string
```

Get a free Groq API key at: https://console.groq.com/keys

**4. Run the app**
```bash
python run.py
```

Open `http://localhost:5000`

---

## Project Structure

```
skillnexora/
├── app/
│   ├── __init__.py        → Flask app setup
│   ├── models.py          → Database tables
│   ├── helpers.py         → Gemini API + streak + badge logic
│   ├── routes/
│   │   ├── auth.py        → Login & Signup
│   │   ├── main.py        → Dashboard
│   │   ├── learning.py    → Learning Tracker
│   │   ├── post.py        → Post Generator
│   │   ├── outreach.py    → Cold Outreach
│   │   └── streak.py      → Streak & Badges
│   ├── templates/         → HTML pages
│   └── static/            → CSS styles
├── .github/
│   ├── ISSUE_TEMPLATE/    → Bug, Feature, Docs templates
│   └── PULL_REQUEST_TEMPLATE.md
├── .env.example
├── requirements.txt
├── run.py
└── README.md
```

---

## Want to Contribute?

We welcome all contributors — beginners welcome! 🙌

1. Look for issues labeled `good first issue`
2. Comment that you want to work on it
3. Fork → make changes → open PR

Read [CONTRIBUTING.md](CONTRIBUTING.md) before you start.

---

## License

MIT License
