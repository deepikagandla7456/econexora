# How to Contribute to SkillNexora 🙌

Thanks for wanting to help! Here's everything in simple steps.

---

## Step 1 — Find an issue

Go to the [Issues tab](../../issues) and look for:
- `good first issue` → perfect if you're new
- `enhancement` → for adding features
- `bug` → for fixing broken things

Comment: **"I'd like to work on this!"** and wait to be assigned before starting.

---

## Step 2 — Fork and clone

Click **Fork** on the top right, then:
```bash
git clone https://github.com/YOUR_USERNAME/skillnexora.git
cd skillnexora
```

---

## Step 3 — Set up locally

```bash
pip install -r requirements.txt
```

Create a `.env` file (copy from `.env.example`):
```
GROQ_API_KEY=your_key_here
SECRET_KEY=any_random_string
```

Run the app:
```bash
python run.py
```

Open `http://localhost:5000` in your browser.

---

## Step 4 — Make your changes

```bash
git checkout -b your-branch-name
```

Make changes, test that the app still runs, then:
```bash
git add .
git commit -m "short description of your change"
git push origin your-branch-name
```

---

## Step 5 — Open a Pull Request

Go to GitHub and open a PR. Fill in the PR template — it helps us review faster!

---

## Simple rules

- One issue per PR please
- Don't change files not related to your issue
- Test before submitting
- Be kind 🙂

---

Need help? Comment on your issue or open a [Discussion](../../discussions).
