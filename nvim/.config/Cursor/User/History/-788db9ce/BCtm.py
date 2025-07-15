import pytest
from signalwire import SignalWireClient
from menu.cli import CallDetails
import os
import requests
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_call_details():
    """Fixture to create test call details."""
    return CallDetails(
        phone_number="+1234567890",
        contact_name="Test Contact",
        objective="Test call",
        caller_name="Test Caller",
        additional_context="Test context"
    )

@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to set up test environment variables."""
    monkeypatch.setenv("TEST_PHONE_NUMBER", "16145572867")
    monkeypatch.setenv("SIGNALWIRE_API_KEY", "PT123.456")

@pytest.fixture
def client(mock_env):
    """Fixture to create SignalWire client with test API key."""
    return SignalWireClient()

def test_client_initialization(mock_env):
    """Test that client can be initialized with API key."""
    client = SignalWireClient()
    assert client.api_key == "PT123.456"
    assert client.project_id == "PT123"
    assert client.phone_number == "+16145572867"
    assert "saorsadev.signalwire.com" in client.base_url
    assert "/api/laml/2010-04-01/Accounts/PT123" in client.base_url

def test_missing_phone_number(monkeypatch):
    """Test that client raises error when TEST_PHONE_NUMBER is not set."""
    monkeypatch.setenv("SIGNALWIRE_API_KEY", "PT123.456")
    monkeypatch.delenv("TEST_PHONE_NUMBER", raising=False)
    
    with pytest.raises(ValueError) as exc_info:
        SignalWireClient()
    assert "TEST_PHONE_NUMBER environment variable must be set" in str(exc_info.value)

def test_create_prompt(client, mock_call_details):
    """Test that prompt is created correctly from call details."""
    prompt = client._create_prompt(mock_call_details)
    assert mock_call_details.caller_name in prompt
    assert mock_call_details.contact_name in prompt
    assert mock_call_details.objective in prompt
    assert mock_call_details.additional_context in prompt
    # Check format
    assert prompt.startswith("Hello, this is")
    assert "calling" in prompt

@patch('requests.post')
def test_make_call_payload(mock_post, client, mock_call_details):
    """Test that make_call creates correct payload without making actual API call."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "test-call-id"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    # Make test call
    response = client.make_call(mock_call_details)
    
    # Verify request was made with correct data
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    
    # Check URL
    assert "saorsadev.signalwire.com" in call_args[0][0]
    assert "/Calls" in call_args[0][0]
    
    # Check payload
    payload = call_args[1]["data"]
    assert "To" in payload
    assert "From" in payload
    assert payload["From"] == "+16145572867"  # Check that it's using the env var
    assert "Twiml" in payload
    assert "<?xml" in payload["Twiml"]
    assert "<Response>" in payload["Twiml"]
    assert "<Say>" in payload["Twiml"]
    
    # Check headers
    headers = call_args[1]["headers"]
    assert "Content-Type" in headers
    assert headers["Content-Type"] == "application/x-www-form-urlencoded"
    assert "Accept" in headers
    assert headers["Accept"] == "application/json"
    
    # Check auth
    auth = call_args[1]["auth"]
    assert auth == ("PT123", "PT123.456")
    
    # Check response
    assert response == {"id": "test-call-id"}

@patch('requests.post')
def test_make_call_handles_errors(mock_post, client, mock_call_details):
    """Test that make_call handles API errors gracefully."""
    # Setup mock to raise an error
    mock_post.side_effect = requests.exceptions.RequestException("API Error")
    
    # Verify error is raised with our custom message
    with pytest.raises(RuntimeError) as exc_info:
        client.make_call(mock_call_details)
    assert "Failed to initiate SignalWire call" in str(exc_info.value) 