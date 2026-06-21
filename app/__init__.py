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
    
    # Configure Database: Use environment key with PostgreSQL fallback support
    db_uri = os.getenv("DATABASE_URL")
    if not db_uri:
        if os.getenv("VERCEL"):
            db_uri = "sqlite:////tmp/skillnexora.db"
        else:
            db_uri = "sqlite:///skillnexora.db"
            
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Configure Connection Pooling (Efficiency Upgrade for PostgreSQL)
    if not db_uri.startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_size": 10,
            "pool_recycle": 1800,
            "pool_pre_ping": True
        }

    # Custom CSRF Protection (Security Upgrade)
    import secrets
    from flask import session, request, abort

    @app.before_request
    def csrf_protect():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(32)
        
        if request.method == "POST" and not app.config.get("TESTING"):
            token = request.form.get("csrf_token")
            if not token or token != session.get("csrf_token"):
                abort(400, "CSRF token missing or invalid.")

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=session.get("csrf_token", ""))

    # Gzip Response Compression Middleware (Efficiency Upgrade)
    import gzip
    @app.after_request
    def compress_response(response):
        accept_encoding = request.headers.get("Accept-Encoding", "")
        if (
            "gzip" not in accept_encoding.lower()
            or response.status_code < 200
            or response.status_code >= 300
            or "Content-Encoding" in response.headers
        ):
            return response

        response.direct_passthrough = False
        content = gzip.compress(response.get_data())
        response.set_data(content)
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = str(len(content))
        return response

    db.init_app(app)
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

    with app.app_context():
        db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

