"""
Anthropic Claude model implementation.
"""
from typing import Optional
import os
from pathlib import Path
import anthropic
from dotenv import load_dotenv
from rich import print as rprint
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
        
        # Load environment variables from .env file
        env_path = Path(__file__).parent.parent / '.env'
        rprint(f"[yellow]Looking for .env file at:[/yellow] {env_path}")
        rprint(f"[yellow]File exists:[/yellow] {env_path.exists()}")
        
        if env_path.exists():
            try:
                with open(env_path, 'r') as f:
                    content = f.read().strip()
                    rprint(f"[yellow].env file content length:[/yellow] {len(content)} characters")
                    rprint(f"[yellow]First line starts with:[/yellow] {content.split('\\n')[0][:10]}...")
            except Exception as e:
                rprint(f"[red]Error reading .env file:[/red] {str(e)}")
        
        # Try loading with explicit path
        load_dotenv(dotenv_path=str(env_path.absolute()))
        
        # Debug: Check if key was loaded
        api_key = os.getenv("ANTHROPIC_API_KEY")
        rprint(f"[yellow]API key found in environment:[/yellow] {'Yes' if api_key else 'No'}")
        if not api_key:
            rprint("[red]Warning: ANTHROPIC_API_KEY not found in .env file[/red]")
        
    def load_model(self) -> None:
        """Initialize the Anthropic client if not already done."""
        if self.client is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in .env file")
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