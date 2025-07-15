import pytest
from web import create_app
from database import init_db, get_db_session, User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Create a test user in the database."""
    with app.app_context():
        init_db()
        session = get_db_session()
        user = User(
            email='test@example.com',
            password_hash=generate_password_hash('testpass123'),
            full_name='Test User'
        )
        session.add(user)
        session.commit()
        session.close()
        return user

def test_home_page(client):
    """Test the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200, "Home page request failed"
    assert b'Welcome to PyDial' in response.data, "Home page title not found"
    assert b'Your AI-powered calling assistant' in response.data, "Home page tagline not found"

def test_about_page(client):
    """Test the about page loads correctly."""
    response = client.get('/about')
    assert response.status_code == 200, "About page request failed"
    assert b'About PyDial' in response.data, "About page title not found"
    assert b'What is PyDial?' in response.data, "About page section not found"
    assert b'How It Works' in response.data, "How It Works section not found"

def test_login_page(client):
    """Test the login page loads correctly."""
    response = client.get('/login')
    assert response.status_code == 200, "Login page request failed"
    assert b'Login' in response.data, "Login page title not found"
    assert b'Email' in response.data, "Email field not found"
    assert b'Password' in response.data, "Password field not found"

def test_signup_page(client):
    """Test the signup page loads correctly."""
    response = client.get('/signup')
    assert response.status_code == 200, "Signup page request failed"
    assert b'Sign Up' in response.data, "Signup page title not found"
    assert b'Email' in response.data, "Email field not found"
    assert b'Password' in response.data, "Password field not found"

def test_stripe_page(client):
    """Test the stripe page loads correctly."""
    response = client.get('/stripe')
    assert response.status_code == 200, "Stripe page request failed"
    assert b'Upgrade Your Plan' in response.data, "Stripe page title not found"
    assert b'Stripe integration coming soon!' in response.data, "Stripe placeholder not found" 