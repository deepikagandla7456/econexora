from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-this")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///skillnexora.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."
    login_manager.login_message_category = "info"

    from app.routes.auth import auth
    from app.routes.learning import learning
    from app.routes.post import post
    from app.routes.outreach import outreach
    from app.routes.streak import streak
    from app.routes.main import main

    app.register_blueprint(auth)
    app.register_blueprint(learning)
    app.register_blueprint(post)
    app.register_blueprint(outreach)
    app.register_blueprint(streak)
    app.register_blueprint(main)

    # with app.app_context():
        # db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    return None
