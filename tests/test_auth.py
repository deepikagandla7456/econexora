import unittest
from app import create_app, db
from app.models import User
import os

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        os.environ["SECRET_KEY"] = "test-secret"
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_page_loads(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create Account", response.data)

    def test_login_page_loads(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_signup_successful(self):
        response = self.client.post("/signup", data={
            "username": "testuser",
            "email": "test@arenaops.com",
            "password": "testpassword"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            user = User.query.filter_by(email="test@arenaops.com").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser")

    def test_login_successful(self):
        self.client.post("/signup", data={
            "username": "testuser2",
            "email": "test2@arenaops.com",
            "password": "testpassword"
        })
        response = self.client.post("/login", data={
            "email": "test2@arenaops.com",
            "password": "testpassword"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_demo_mode_successful(self):
        response = self.client.get("/demo", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"demo_", response.data)
