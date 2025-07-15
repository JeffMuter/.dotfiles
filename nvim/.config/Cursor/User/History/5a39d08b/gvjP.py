"""
Route handlers for the web interface.
"""
from flask import render_template

def register_routes(app):
    """Register all route handlers."""
    
    @app.route('/')
    def home():
        """Homepage route."""
        return render_template('index.html') 