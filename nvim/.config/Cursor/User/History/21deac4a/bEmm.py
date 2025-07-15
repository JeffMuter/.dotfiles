"""
Inference package for handling LLM interactions.
"""
from typing import Literal
from .base import LLMInterface
from .tiny_llama import TinyLlamaModel
from .anthropic_model import AnthropicModel

ModelType = Literal["tiny-llama", "anthropic"]

def create_model(model_type: ModelType = "anthropic") -> LLMInterface:
    """Create a model instance based on the specified type.
    
    Args:
        model_type: Which model implementation to use
        
    Returns:
        An instance of the specified model
    """
    if model_type == "tiny-llama":
        return TinyLlamaModel()
    elif model_type == "anthropic":
        return AnthropicModel()
    else:
        raise ValueError(f"Unknown model type: {model_type}")

__all__ = ['LLMInterface', 'TinyLlamaModel', 'AnthropicModel', 'create_model'] 