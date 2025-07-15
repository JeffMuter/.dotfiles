"""
Tests for authentication functionality.
"""
import pytest
from web.app import create_app
from database.db import init_db, get_db_session
from database.models import User
from werkzeug.security import check_password_hash

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
    })
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def db_session():
    """Create a database session for testing."""
    session = get_db_session()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    # Clean up any existing test users first
    db_session.query(User).filter_by(email='user@user.com').delete()
    db_session.query(User).filter_by(username='testuser').delete()
    db_session.commit()
    
    user = User(
        username='testuser',
        email='user@user.com'
    )
    user.set_password('useruser')
    db_session.add(user)
    db_session.commit()
    return user

def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post('/auth/login', data={
        'email': 'user@user.com',
        'password': 'useruser'
    }, follow_redirects=True)
    assert response.status_code == 200, "Login request failed"
    assert 'Login successful!' in response.get_data(as_text=True), "Login success message not found"

def test_login_wrong_password(client, test_user):
    """Test login with wrong password."""
    response = client.post('/auth/login', data={
        'email': 'user@user.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200, "Login request failed"
    assert 'Invalid email or password' in response.get_data(as_text=True), "Wrong password error not shown"

def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post('/auth/login', data={
        'email': 'nonexistent@user.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200, "Login request failed"
    assert 'Invalid email or password' in response.get_data(as_text=True), "Non-existent user error not shown"

def test_signup_success(client, db_session):
    """Test successful user registration."""
    # Clean up any existing test users first
    db_session.query(User).filter_by(email='new@user.com').delete()
    db_session.query(User).filter_by(username='newuser').delete()
    db_session.commit()
    
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@user.com',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200, "Registration request failed"
    assert 'Registration successful!' in response.get_data(as_text=True), "Success message not shown"
    
    # Verify user was created in database
    user = db_session.query(User).filter_by(email='new@user.com').first()
    assert user is not None, "User was not created in database"
    assert user.username == 'newuser', "Username mismatch in database"

def test_signup_duplicate_email(client, test_user):
    """Test registration with existing email."""
    response = client.post('/auth/register', data={
        'username': 'another',
        'email': 'user@user.com',  # Same as test_user
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200, "Registration request failed"
    assert 'Email already registered' in response.get_data(as_text=True), "Duplicate email error not shown"

def test_signup_duplicate_username(client, test_user):
    """Test registration with existing username."""
    response = client.post('/auth/register', data={
        'username': 'testuser',  # Same as test_user
        'email': 'another@user.com',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200, "Registration request failed"
    assert b'Username already taken' in response.data, "Duplicate username error message not found"

def test_signup_password_mismatch(client):
    """Test registration with mismatched passwords."""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@user.com',
        'password': 'password123',
        'password2': 'different123'
    }, follow_redirects=True)
    assert response.status_code == 200, "Registration request failed"
    assert b'Field must be equal to password' in response.data, "Password mismatch error message not found"

def test_logout(client, test_user):
    """Test logout functionality."""
    # First login
    login_response = client.post('/auth/login', data={
        'email': 'user@user.com',
        'password': 'useruser'
    })
    assert login_response.status_code == 302, "Login redirect failed"
    
    # Then logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200, "Logout request failed"
    assert b'You have been logged out' in response.data, "Logout message not found"

def test_signup(client):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful!' in response.data
    
    # Check if user was created in database
    session = get_db_session()
    user = session.query(User).filter_by(email='new@example.com').first()
    session.close()
    
    assert user is not None
    assert user.username == 'newuser'

def test_login(client, test_user):
    """Test user login."""
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Welcome back' in response.data

def test_login_invalid_password(client, test_user):
    """Test login with invalid password."""
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpass'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

def test_signup_existing_email(client, test_user):
    """Test signup with existing email."""
    response = client.post('/signup', data={
        'name': 'Another User',
        'email': 'test@example.com',  # Same as test_user
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Email already registered' in response.data

def test_password_mismatch(client):
    """Test signup with mismatched passwords."""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'password2': 'different123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Field must be equal to password' in response.data 