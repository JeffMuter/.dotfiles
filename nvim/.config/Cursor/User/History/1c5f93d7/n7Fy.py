import pytest
from database import get_db_session, User
from werkzeug.security import check_password_hash

def test_signup(client):
    """Test user registration."""
    response = client.post('/signup', data={
        'name': 'New User',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Check if user was created in database
    session = get_db_session()
    user = session.query(User).filter_by(email='new@example.com').first()
    session.close()
    
    assert user is not None
    assert user.full_name == 'New User'
    assert check_password_hash(user.password_hash, 'password123')

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
    response = client.post('/signup', data={
        'name': 'New User',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'different123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Passwords do not match' in response.data 