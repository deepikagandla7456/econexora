import unittest
from app import create_app, db
from app.models import User, Learning, Streak, Badge
from app.helpers import build_skill_profile, update_streak, check_and_award_badges
from datetime import date, timedelta
import os

class HelpersTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["SECRET_KEY"] = "test-secret"
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        self.app = create_app()
        self.app.config["TESTING"] = True
        
        with self.app.app_context():
            db.create_all()
            self.user = User(username="testuser", email="test@econexora.com", password="hashed_password")
            db.session.add(self.user)
            db.session.commit()
            self.user_id = self.user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_build_skill_profile(self):
        with self.app.app_context():
            l1 = Learning(user_id=self.user_id, title="Eco", platform="Transport", resource_type="low", topic="0.8 kg CO2", skills="Low-Carbon", progress=100, time_spent=5)
            l2 = Learning(user_id=self.user_id, title="Meat", platform="Food", resource_type="high", topic="6.2 kg CO2", skills="High-Impact", progress=100, time_spent=2)
            db.session.add_all([l1, l2])
            db.session.commit()
            
            user = db.session.get(User, self.user_id)
            profile = build_skill_profile(user.learnings)
            self.assertIn("Total CO2 Emissions: 7.0 kg CO2", profile)
            self.assertIn("Low-Carbon", profile)

    def test_get_carbon_profile_data(self):
        with self.app.app_context():
            l1 = Learning(user_id=self.user_id, title="Eco", platform="Transport", resource_type="low", topic="0.8 kg CO2", skills="Low-Carbon", progress=100, time_spent=5)
            l2 = Learning(user_id=self.user_id, title="Meat", platform="Food", resource_type="high", topic="6.2 kg CO2", skills="High-Impact", progress=100, time_spent=2)
            db.session.add_all([l1, l2])
            db.session.commit()
            
            user = db.session.get(User, self.user_id)
            from app.helpers import get_carbon_profile_data
            data = get_carbon_profile_data(user.learnings)
            self.assertEqual(data["total_emissions"], 7.0)
            self.assertEqual(data["count"], 2)
            self.assertEqual(data["total_quantity"], 7.0)
            self.assertIn("Low-Carbon", data["impact_tags"])
            self.assertIn("Transport", data["categories"])

    def test_update_streak_new(self):
        with self.app.app_context():
            user = db.session.get(User, self.user_id)
            update_streak(user)
            self.assertIsNotNone(user.streak)
            self.assertEqual(user.streak.current_streak, 1)

    def test_update_streak_consecutive(self):
        with self.app.app_context():
            user = db.session.get(User, self.user_id)
            streak = Streak(user_id=user.id, current_streak=1, longest_streak=1, last_logged=date.today() - timedelta(days=1))
            db.session.add(streak)
            db.session.commit()
            
            update_streak(user)
            self.assertEqual(user.streak.current_streak, 2)

    def test_check_and_award_badges(self):
        with self.app.app_context():
            user = db.session.get(User, self.user_id)
            streak = Streak(user_id=user.id, current_streak=7, longest_streak=7, last_logged=date.today())
            db.session.add(streak)
            db.session.commit()
            
            check_and_award_badges(user)
            badge_names = [b.name for b in user.badges]
            self.assertIn("7-Day Streak", badge_names)
