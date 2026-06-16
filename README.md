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

## 🤝 Contributing Guide

We welcome contributions from beginners 💙

### 🔰 Steps to Contribute

1. Go to the **Issues** section
2. Choose an issue to work on
3. Comment to get assigned
4. Fork the repository
5. Create a new branch

```
git checkout -b feature/your-feature-name
```

6. Make your changes
7. Commit changes

```
git commit -m "Added: your feature name"
```

8. Push to GitHub

```
git push origin feature/your-feature-name
```

9. Create a Pull Request 🎉

---

## 📌 Contribution Guidelines

* ✅ Keep code clean and readable
* ✅ Follow proper folder structure
* ✅ Make components responsive
* ✅ Use meaningful commit messages
* ✅ Avoid breaking existing UI
* ✅ Add comments where necessary

---

## 🧩 Contribution Areas


### 🎨 UI Improvements

* Improve responsiveness
* Add animations
* Enhance UX/UI
* Improve mobile experience

---

### ⚙️ Features

* Add new component pages
* Improve code preview system
* Add dark mode 🌙
* Improve sidebar navigation
* Add search functionality

---

## 🏷️ Issue Labels

* `good first issue` → Beginner-friendly
* `enhancement` → Feature request
* `bug` → Bug fixes
* `documentation` → Docs improvements

---

## 💡 Example Contributions

* Create a responsive navbar
* Add hover effects to cards
* Improve mobile layout
* Add new UI components

---

## 🎯 Project Goals

* Help beginners start open-source contributions
* Build a large UI component library
* Create a developer-friendly UI showcase platform

---

## ⭐ Support

If you like this project:

* Give it a ⭐
* Share it with others
* Contribute 🚀

## 👨‍💻 Maintainer

**Project Admin:** Deepika Gandla


---

<h2 align="center"> 💙 Happy Coding & Contributing! </h2>

---
