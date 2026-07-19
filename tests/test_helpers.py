import unittest
from app import create_app, db
from app.models import User, OperationLog, Streak, Badge
from app.helpers import build_skill_profile, get_operations_profile_data, update_streak, check_and_award_badges
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
            self.user = User(username="testuser", email="test@arenaops.com", password="hashed_password")
            db.session.add(self.user)
            db.session.commit()
            self.user_id = self.user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_build_skill_profile(self):
        with self.app.app_context():
            l1 = OperationLog(user_id=self.user_id, title="Queue gate 3", category="Gates", severity="low", location="Gate 3 Entrance", actions_taken="Added staff", resolution_progress=100, response_time=5.0)
            l2 = OperationLog(user_id=self.user_id, title="Lot B full", category="Parking", severity="high", location="Parking Lot B", actions_taken="Closed lot", resolution_progress=100, response_time=10.0)
            db.session.add_all([l1, l2])
            db.session.commit()
            
            user = db.session.get(User, self.user_id)
            profile = build_skill_profile(user.operation_logs)
            self.assertIn("Total Incident Logged: 2", profile)
            self.assertIn("Average Operator Response Time: 7.5 mins", profile)

    def test_get_operations_profile_data(self):
        with self.app.app_context():
            l1 = OperationLog(user_id=self.user_id, title="Queue gate 3", category="Gates", severity="low", location="Gate 3 Entrance", actions_taken="Added staff", resolution_progress=100, response_time=5.0)
            l2 = OperationLog(user_id=self.user_id, title="Lot B full", category="Parking", severity="high", location="Parking Lot B", actions_taken="Closed lot", resolution_progress=100, response_time=10.0)
            db.session.add_all([l1, l2])
            db.session.commit()
            
            user = db.session.get(User, self.user_id)
            data = get_operations_profile_data(user.operation_logs)
            self.assertEqual(data["total_response_time"], 15.0)
            self.assertEqual(data["count"], 2)
            self.assertEqual(data["average_response_time"], 7.5)
            self.assertIn("high", data["severities"])
            self.assertIn("Parking", data["categories"])

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
