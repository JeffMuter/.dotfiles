"""
Main Flask application module.
"""
from flask import Flask
from flask_login import LoginManager
from .routes import register_routes
from .auth import auth_bp, login_manager
from database.db import init_db
import os

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')  # Change in production!
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    register_routes(app)
    
    return app

def run_web_interface():
    """Run the web interface."""
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 