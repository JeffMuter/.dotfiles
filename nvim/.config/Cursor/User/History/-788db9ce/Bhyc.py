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
def client():
    """Fixture to create SignalWire client with test API key."""
    api_key = os.environ.get("SIGNALWIRE_API_KEY")
    if not api_key:
        pytest.skip("SIGNALWIRE_API_KEY not set in environment")
    return SignalWireClient(api_key=api_key)

def test_client_initialization():
    """Test that client can be initialized with API key from env."""
    api_key = os.environ.get("SIGNALWIRE_API_KEY")
    if not api_key:
        pytest.skip("SIGNALWIRE_API_KEY not set in environment")
    
    client = SignalWireClient(api_key=api_key)
    assert client.api_key == api_key
    assert "saorsadev.signalwire.com" in client.base_url

def test_create_prompt(client, mock_call_details):
    """Test that prompt is created correctly from call details."""
    prompt = client._create_prompt(mock_call_details)
    assert mock_call_details.caller_name in prompt
    assert mock_call_details.contact_name in prompt
    assert mock_call_details.objective in prompt
    assert mock_call_details.additional_context in prompt

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
    
    # Check payload
    payload = call_args[1]["json"]
    assert "to" in payload
    assert "from" in payload
    assert "ai_voice" in payload
    assert isinstance(payload["ai_voice"], dict)
    assert "prompt" in payload["ai_voice"]
    
    # Check headers
    headers = call_args[1]["headers"]
    assert "Authorization" in headers
    assert "Bearer" in headers["Authorization"]
    assert "Content-Type" in headers
    assert headers["Content-Type"] == "application/json"
    
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