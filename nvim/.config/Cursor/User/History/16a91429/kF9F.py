"""
Base interface for LLM interactions.
"""
from abc import ABC, abstractmethod
from typing import Optional

class LLMInterface(ABC):
    """Abstract base class for LLM interactions."""
    
    @abstractmethod
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """
        Generate a response from the LLM based on the input prompt.
        
        Args:
            prompt: The input prompt to generate from
            max_length: Optional maximum length for the generated response
            
        Returns:
            str: The generated response
        """
        pass
    
    @abstractmethod
    def load_model(self) -> None:
        """
        Load the model into memory.
        Should be called before first generation.
        """
        pass 