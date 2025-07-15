import pytest
from inference.anthropic_model import AnthropicModel
import os

def test_anthropic_model_response():
    """Test that the AnthropicModel can generate a basic response."""
    # Skip if no API key is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not set in environment")
    
    # Initialize the model
    model = AnthropicModel()
    
    # Create a simple test prompt
    test_prompt = """Calling: Test Contact
Contact: John Doe
Objective: Test if the model responds
Additional Context: This is a test call"""
    
    # Generate a response
    response = model.generate_response(test_prompt)
    
    # Basic assertions
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Print the response for manual inspection
    print(f"\nReceived response: {response}") 