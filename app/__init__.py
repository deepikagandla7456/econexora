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

    # Session Cookie Security Configuration
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Unified Security Headers, Caching, and Compression Middleware
    import gzip
    @app.after_request
    def optimize_and_secure_response(response):
        # 1. Inject HTTP Security Headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "font-src 'self' https://cdnjs.cloudflare.com; "
            "img-src 'self' data:; "
            "frame-ancestors 'none';"
        )

        # 2. Inject Caching Headers
        # Cache static files aggressively; prevent caching on dynamic paths to ensure user state is fresh.
        if request.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"

        # 3. Gzip Compression (if accepted by client)
        accept_encoding = request.headers.get("Accept-Encoding", "")
        content_type = response.headers.get("Content-Type", "")
        is_compressible = any(t in content_type for t in ["text/html", "text/css", "application/javascript", "application/json"])

        if (
            "gzip" in accept_encoding.lower()
            and response.status_code >= 200
            and response.status_code < 300
            and "Content-Encoding" not in response.headers
            and is_compressible
        ):
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
    return db.session.get(User, int(user_id))

