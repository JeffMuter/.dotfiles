import pytest
from unittest.mock import patch
from menu.cli import CallDetails, make_call_menu

@pytest.fixture
def mock_env(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("TARGET_PHONE_NUMBER", "1234567890")

@pytest.fixture
def mock_prompt_responses():
    """Fixture to simulate user input in the menu."""
    return {
        "caller_name": "Test Caller",
        "contact_name": "Test Contact",
        "objective": "Discuss weather",
        "additional_context": "Friendly conversation"
    }

def test_make_call_menu_basic(mock_env, mock_prompt_responses):
    """Test the basic functionality of make_call_menu with all fields filled."""
    # Patch rich.prompt.Prompt.ask to return our mock responses
    with patch('rich.prompt.Prompt.ask') as mock_ask:
        # Configure mock to return values in sequence
        mock_ask.side_effect = [
            mock_prompt_responses["caller_name"],
            mock_prompt_responses["contact_name"],
            mock_prompt_responses["objective"],
            mock_prompt_responses["additional_context"]
        ]
        
        # Call the function
        result = make_call_menu()
        
        # Verify the result
        assert isinstance(result, CallDetails)
        assert result.phone_number == "+11234567890"  # Should be formatted from environment
        assert result.contact_name == mock_prompt_responses["contact_name"]
        assert result.objective == mock_prompt_responses["objective"]
        assert result.additional_context == mock_prompt_responses["additional_context"]

def test_make_call_menu_minimal(mock_env, mock_prompt_responses):
    """Test make_call_menu with minimal input (no additional context)."""
    with patch('rich.prompt.Prompt.ask') as mock_ask:
        # Configure mock to return values in sequence, with empty additional context
        mock_ask.side_effect = [
            mock_prompt_responses["caller_name"],
            mock_prompt_responses["contact_name"],
            mock_prompt_responses["objective"],
            ""  # Empty additional context
        ]
        
        # Call the function
        result = make_call_menu()
        
        # Verify the result
        assert isinstance(result, CallDetails)
        assert result.phone_number == "+11234567890"  # Should be formatted from environment
        assert result.contact_name == mock_prompt_responses["contact_name"]
        assert result.objective == mock_prompt_responses["objective"]
        assert result.additional_context is None  # Should be None when not provided

def test_missing_target_number(monkeypatch):
    """Test that menu raises error when TARGET_PHONE_NUMBER is not set."""
    # Ensure TARGET_PHONE_NUMBER is not set
    monkeypatch.delenv("TARGET_PHONE_NUMBER", raising=False)
    
    with pytest.raises(ValueError) as exc_info:
        make_call_menu()
    assert "TARGET_PHONE_NUMBER environment variable must be set" in str(exc_info.value)

def test_invalid_target_number(monkeypatch):
    """Test that menu raises error when TARGET_PHONE_NUMBER is invalid."""
    monkeypatch.setenv("TARGET_PHONE_NUMBER", "123")  # Too short
    
    with pytest.raises(ValueError) as exc_info:
        make_call_menu()
    assert "Invalid TARGET_PHONE_NUMBER" in str(exc_info.value) 