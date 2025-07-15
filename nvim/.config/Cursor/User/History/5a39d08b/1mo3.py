"""
Route handlers for the web interface.
"""
from flask import render_template, redirect, url_for
from flask_login import login_required
from datetime import datetime

def register_routes(app):
    """Register all route handlers."""
    
    @app.route('/')
    def home():
        """Homepage route."""
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        """About page route."""
        return render_template('about.html')
    
    # Redirect old auth routes to new ones
    @app.route('/login')
    def login_redirect():
        """Redirect old login route to new auth login route."""
        return redirect(url_for('auth.login'))
    
    @app.route('/signup')
    def signup_redirect():
        """Redirect old signup route to new auth register route."""
        return redirect(url_for('auth.register'))
    
    @app.route('/stripe')
    @login_required
    def stripe_page():
        """Stripe payment page route."""
        return render_template('stripe.html')
    
    # Template context processor to add current year to all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow} 