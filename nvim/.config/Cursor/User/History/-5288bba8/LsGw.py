"""
Main Flask application module.
"""
from flask import Flask
from .routes import register_routes

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Register routes
    register_routes(app)
    
    return app

def run_web_interface():
    """Run the web interface."""
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 