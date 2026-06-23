# EcoNexora 🌿
> AI-powered Carbon Footprint Awareness and Tracking Platform that drives personal climate action.

EcoNexora is a carbon footprint accounting and awareness platform built for the Hack2Skills Prompt Wars. It empowers individuals to log their daily activities (transport, meals, electricity consumption), utilizes AI to extract environmental impacts and estimate emissions, builds a green profile, and generates copy-ready climate posts and sustainability outreach messages.



---

## 🎯 Hack2Skills Submission Details

*   **Chosen Vertical**: Sustainability / Green Tech / Carbon Footprint Awareness
*   **Target Users**: Eco-conscious citizens, green advocates, sustainability students, ESG job seekers, and climate organizations.

### 🧠 Approach & Logic

1.  **AI Carbon Impact & Emissions Extraction**:
    *   **Logic**: When an eco-activity is logged, the raw details (e.g. "vegan burger lunch" or "diesel bus commute") are processed. The **Groq API** (`llama-3.3-70b-versatile`) calculates estimated emissions (in kg CO2) and returns environmental impact tags.
    *   **Impact**: Simplifies carbon accounting by converting natural language activity titles into concrete CO2 equivalents.
2.  **Gamification (Eco-Streaks & Green Badges)**:
    *   **Logic**: The system checks the last logged date. Continuous logging increments the "Green Streak." Reaching milestone streaks awards badges like **Eco Champion** (offsetting 5 logs) and **7-Day Streak**.
    *   **Impact**: Reinforces consistent tracking habits using positive gamified rewards.
3.  **Sustainability Content & Outreach Pipeline**:
    *   **Logic**: The system summarizes the user's logged categories, offsets, and emissions data. This context is used by the AI engine to generate professional LinkedIn eco-posts, X/Twitter threads, and personalized DMs targeting Sustainability Managers or ESG companies.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python + Flask |
| **Database** | PostgreSQL / SQLite (Local Fallback) |
| **Authentication** | Flask-Login |
| **AI Inference** | Groq API (Llama 3 Models) |
| **Frontend** | HTML5, CSS3, JavaScript, Tailwind CSS, Jinja2 Templates |

---

## ✨ Features Overview

*   **🌿 Carbon Tracker**: Log daily footprint items (Category: Transport, Food, Energy, Waste, Water, Shopping). Track offset progress.
*   **🔥 Eco-Streak & Badges**: Consistent logging builds streak multiplier and awards unlockable green badges.
*   **✍️ AI Eco Post Generator**: Instantly generate structured LinkedIn articles or Twitter threads advocating personal carbon metrics.
*   **📩 AI Climate Outreach**: Personalize outreach DMs to Sustainability Leads, ESG Leads, and environmental non-profits.
*   **🚀 Demo Mode**: Explorable guest access seeded with transport and energy carbon logs.

---

## ⚙️ Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/deepikagandla7456/skillnexora.git
cd skillnexora
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
skillnexora/
├── app/
│   ├── __init__.py        → Flask App factory and DB context setup
│   ├── models.py          → SQLAlchemy Database models
│   ├── helpers.py         → Groq LLM eco-prompts and streak logic
│   ├── demo_data.py       → Seeds carbon tracking logs for Demo Mode
│   ├── routes/            → Blueprint routes
│   │   ├── auth.py        → Auth & Demo login
│   │   ├── main.py        → Home & Dashboard
│   │   ├── learning.py    → Carbon Tracker routes
│   │   ├── post.py        → AI Eco Post Generation
│   │   ├── outreach.py    → AI Climate Outreach
│   │   └── streak.py      → Gamified eco-badges wall
│   ├── templates/         → Jinja2 HTML Layouts
│   └── static/            → Style sheets
├── requirements.txt       → Library dependencies
├── vercel.json            → Serverless deployment configuration
└── run.py                 → Development server entry point
```

---

## 🔍 Assumptions & Fallbacks

*   **API Accessibility**: Assumes valid `GROQ_API_KEY` for LLM tasks. If missing or invalid, the app catches the exception gracefully and continues to run.
*   **Storage Fallback**: Defaults to local SQLite database if no PostgreSQL `DATABASE_URL` is set, enabling zero-config local runs.
