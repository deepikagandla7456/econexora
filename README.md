# StadiumOps AI 🏟️
> AI-powered telemetry hub, incident dispatcher, and public broadcast assistant for Smart Stadium & Tournament Operations.

StadiumOps AI is a real-time event operations dashboard and crew dispatch platform built for the Hack2Skills Prompt Wars. It empowers stadium operators and tournament directors to log live incidents (gate wait times, parking capacities, concessions, security events), utilizes AI to extract operational insights and draft spectator broadcasts, builds an operator profile, and generates copy-ready staff alert DMs and check-in instructions.

---

## 🎯 Hack2Skills Submission Details

*   **Chosen Vertical**: Smart Stadium & Tournament Operations
*   **Target Users**: Stadium managers, event operators, tournament directors, security leads, emergency response crews, and stadium visitors.

### 🧠 Approach & Logic

1.  **Incident & Telemetry Logging**:
    *   **Logic**: Operators log live events (e.g. "Gate 4 queue delays" or "Concourse A liquid spill"). The system records severity level (low, medium, high, critical), location, actions taken, resolution progress, and live IoT sensor URLs.
    *   **Impact**: Simplifies stadium operations monitoring by capturing live, structured telemetry data in one dashboard.
2.  **Gamification (Operator Streaks & Badges)**:
    *   **Logic**: Continuous logging increments the "Operator Streak." Reaching milestone streaks awards badges like **Crisis Manager** (resolving 5 incidents) and **7-Day Streak**.
    *   **Impact**: Reinforces consistent operational logs tracking habits using positive gamified rewards.
3.  **PR Broadcast & Crew Alerts Pipeline**:
    *   **Logic**: The system summarizes the stadium's current active incidents, severities, and locations. The AI engine (`llama-3.3-70b-versatile` via Groq) drafts spectator warnings, public broadcasts, and urgent SMS dispatches/follow-up instructions for dispatching crew teams.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python + Flask |
| **Database** | SQLite (Production serverless-ready SQLite) |
| **Authentication** | Flask-Login |
| **AI Inference** | Groq API (Llama-3.3 Models) |
| **Frontend** | HTML5, CSS3, JavaScript, Vanilla CSS, Jinja2 Templates |

---

## ✨ Features Overview

*   **🏟️ Operations Console**: Log active stadium events (Category: Parking, Gates, Concessions, Security, Medical, Logistics). Track resolution progress sliders.
*   **🏆 Operator Streaks**: Consistent logging builds active streaks and awards unlockable operations achievements.
*   **📢 PR Broadcasts**: Instantly draft spectator instructions, gate redirects, and alert notifications for socials.
*   **🚨 Staff Crew Alerts**: Personalize urgent SMS dispatches and follow-up check-ins to custodial, security, or medical crews.
*   **🚀 Demo Mode**: Ephemeral guest access seeded with mock queue, spill, and parking telemetry logs.

---

## ⚙️ Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/deepikagandla7456/econexora.git
cd econexora
```

**2. Setup Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Create a `.env` file in the root directory (based on `.env.example`):
```ini
SECRET_KEY=your_session_secret_key
GROQ_API_KEY=your_groq_api_key
```

**4. Start the Application**
```bash
python run.py
```
Open [http://localhost:5000](http://localhost:5000) in your web browser.

---

## 📁 Project Structure

```
econexora/
├── app/
│   ├── __init__.py        → Flask App factory and DB context setup
│   ├── models.py          → SQLAlchemy Database models
│   ├── helpers.py         → Groq LLM prompts and streak logic
│   ├── demo_data.py       → Seeds mock telemetry logs for Demo Mode
│   ├── routes/            → Blueprint routes
│   │   ├── auth.py        → Auth & Demo login
│   │   ├── main.py        → Home & Dashboard console
│   │   ├── learning.py    → Operations Log routes
│   │   ├── post.py        → AI PR Broadcast Generator
│   │   ├── outreach.py    → AI Incident Crew Dispatch
│   │   └── streak.py      → Gamified Operator Streaks
│   ├── templates/         → Jinja2 HTML Layouts
│   └── static/            → Style sheets
├── requirements.txt       → Library dependencies
├── vercel.json            → Serverless deployment configuration
└── run.py                 → Development server entry point
```
