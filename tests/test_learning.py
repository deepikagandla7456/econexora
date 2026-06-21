import unittest
from app import create_app, db
from app.models import User, Learning
import os

class LearningTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["SECRET_KEY"] = "test-secret"
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Register a user
            user = User(username="testuser", email="test@econexora.com", password="hashed_password")
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

        # Setup active session mock
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(self.user_id)
            sess["_fresh"] = True

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_learn_page_loads(self):
        response = self.client.get("/learn")
        self.assertEqual(response.status_code, 200)

    def test_add_learning_entry(self):
        response = self.client.post("/learn", data={
            "title": "Bus commute to city",
            "platform": "Transport",
            "resource_type": "medium",
            "topic": "3.2 kg CO2",
            "skills": "Transit, Commuting",
            "progress": "0",
            "time_spent": "15",
            "url": ""
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            entry = Learning.query.filter_by(title="Bus commute to city").first()
            self.assertIsNotNone(entry)
            self.assertEqual(entry.platform, "Transport")
            self.assertEqual(entry.topic, "3.2 kg CO2")

    def test_update_progress(self):
        with self.app.app_context():
            entry = Learning(
                user_id=self.user_id,
                title="Bus commute",
                platform="Transport",
                resource_type="medium",
                topic="3.2 kg CO2",
                skills="Transit",
                progress=0,
                time_spent=15
            )
            db.session.add(entry)
            db.session.commit()
            entry_id = entry.id

        response = self.client.post(f"/learn/update/{entry_id}", data={
            "progress": "80"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        with self.app.app_context():
            updated = db.session.get(Learning, entry_id)
            self.assertEqual(updated.progress, 80)

    def test_delete_entry(self):
        with self.app.app_context():
            entry = Learning(
                user_id=self.user_id,
                title="Bus commute for delete",
                platform="Transport",
                resource_type="medium",
                topic="3.2 kg CO2",
                skills="Transit",
                progress=0,
                time_spent=15
            )
            db.session.add(entry)
            db.session.commit()
            entry_id = entry.id

        response = self.client.post(f"/learn/delete/{entry_id}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            deleted = db.session.get(Learning, entry_id)
            self.assertIsNone(deleted)
