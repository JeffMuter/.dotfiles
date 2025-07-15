"""
Anthropic Claude model implementation.
"""
from typing import Optional
import os
from pathlib import Path
import anthropic
from dotenv import load_dotenv
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
        load_dotenv(env_path)
        
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
            system_prompt = """You are making an outbound phone call. You should:
- Speak in first person, using natural conversational language
- Keep responses brief and focused like a real phone call
- Use a friendly, professional tone
- Respond to what the other person is saying as if in a live conversation
- Handle interruptions and questions naturally
- Never describe actions or narrate - only say what you would actually speak
Do not mention that you are an AI or that this is a simulation."""
            
            # Parse the input prompt for context
            conversation_prompt = prompt.strip()
            
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_length or 150,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {
                        "role": "user", 
                        "content": f"The person you're calling has just said: {conversation_prompt}"
                    }
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            return f"I'm having some technical difficulties with the connection. {str(e)}" 