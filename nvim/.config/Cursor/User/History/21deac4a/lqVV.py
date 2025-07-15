"""
Inference package for handling LLM interactions.
"""
from .base import LLMInterface
from .tiny_llama import TinyLlamaModel

__all__ = ['LLMInterface', 'TinyLlamaModel'] 