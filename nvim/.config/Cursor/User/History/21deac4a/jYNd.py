"""
Inference package for handling LLM interactions.
"""
from typing import Literal, Optional
from .base import LLMInterface
from .tiny_llama import TinyLlamaModel
from .anthropic_model import AnthropicModel

ModelType = Literal["tiny-llama", "anthropic"]

def create_model(model_type: ModelType = "anthropic", api_key: Optional[str] = None) -> LLMInterface:
    """Create a model instance based on the specified type.
    
    Args:
        model_type: Which model implementation to use
        api_key: API key for cloud models (like Anthropic)
        
    Returns:
        An instance of the specified model
    """
    if model_type == "tiny-llama":
        return TinyLlamaModel()
    elif model_type == "anthropic":
        return AnthropicModel(api_key=api_key)
    else:
        raise ValueError(f"Unknown model type: {model_type}")

__all__ = ['LLMInterface', 'TinyLlamaModel', 'AnthropicModel', 'create_model'] 