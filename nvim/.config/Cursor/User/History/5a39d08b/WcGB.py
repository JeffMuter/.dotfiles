"""
Route handlers for the web interface.
"""
from flask import render_template
from datetime import datetime

def register_routes(app):
    """Register all route handlers."""
    
    @app.route('/')
    def home():
        """Homepage route."""
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        """Login page route."""
        return render_template('login.html')
    
    @app.route('/signup')
    def signup():
        """Signup page route."""
        return render_template('signup.html')
    
    @app.route('/stripe')
    def stripe_page():
        """Stripe payment page route."""
        return render_template('stripe.html')
    
    # Template context processor to add current year to all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow} 