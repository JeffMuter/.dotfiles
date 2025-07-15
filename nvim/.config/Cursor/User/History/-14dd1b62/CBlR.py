"""
Anthropic Claude model implementation.
"""
from typing import Optional
import os
import anthropic
from .base import LLMInterface

class AnthropicModel(LLMInterface):
    """Anthropic Claude implementation of the LLM interface."""
    
    def __init__(self, model_name: str = "claude-3-sonnet-20240229"):
        """Initialize the Anthropic client.
        
        Args:
            model_name: The Anthropic model to use. Defaults to claude-3-sonnet.
        """
        self.model_name = model_name
        self.client = None
        
    def load_model(self) -> None:
        """Initialize the Anthropic client if not already done."""
        if self.client is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self.client = anthropic.Anthropic(api_key=api_key)
    
    def unload_model(self) -> None:
        """Clear the client."""
        self.client = None
    
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """Generate a response using Claude.
        
        Args:
            prompt: The input prompt
            max_length: Optional maximum length for the response
        
        Returns:
            str: The generated response
        """
        try:
            if self.client is None:
                self.load_model()
            
            # Format the prompt for a phone conversation
            system_prompt = "You are on a phone call. Respond naturally as if speaking on the phone."
            
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_length or 150,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt.strip()}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            return f"I'm having some technical difficulties with the connection. {str(e)}" 