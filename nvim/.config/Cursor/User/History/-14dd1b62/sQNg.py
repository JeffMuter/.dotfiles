"""
Anthropic Claude model implementation.
"""
from typing import Optional
import os
from pathlib import Path
import anthropic
from rich import print as rprint
from .base import LLMInterface

class AnthropicModel(LLMInterface):
    """Anthropic Claude implementation of the LLM interface."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "claude-3-sonnet-20240229"):
        """Initialize the Anthropic client.
        
        Args:
            api_key: Anthropic API key. If not provided, will try to get from environment.
            model_name: The Anthropic model to use. Defaults to claude-3-sonnet.
        """
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided either directly or via ANTHROPIC_API_KEY environment variable")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def load_model(self) -> None:
        """Nothing to load for API-based model."""
        pass
    
    def unload_model(self) -> None:
        """Nothing to unload for API-based model."""
        pass
    
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """Generate a response using Claude.
        
        Args:
            prompt: The input prompt
            max_length: Optional maximum length for the response
        
        Returns:
            str: The generated response
        """
        try:
            # Format the prompt for a phone conversation
            system_prompt = """You are on a live phone call right now. You must:
1. Speak ONLY in first person, as if actually talking on the phone
2. Say ONLY what you would literally speak out loud
3. Keep responses brief and natural
4. Never narrate or describe actions
5. Never use quotation marks or formatting
6. Never say 'I would say' or similar - just say it
7. Respond directly to what you hear, as in a real conversation"""
            
            # Format as a real phone conversation
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": "You are on a phone call. The other person just said: " + prompt.strip()
                }
            ]
            
            # Debug: Print what we're sending
            rprint("[cyan]Sending to Anthropic:[/cyan]")
            rprint(f"System: {system_prompt}")
            rprint(f"User: {messages[1]['content']}")
            
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_length or 150,
                temperature=0.7,
                system=system_prompt,
                messages=messages
            )
            
            response = message.content[0].text
            
            # Debug: Print what we received
            rprint("[green]Received from Anthropic:[/green]")
            rprint(response)
            
            return response
            
        except Exception as e:
            return f"I'm having some technical difficulties with the connection. {str(e)}" 