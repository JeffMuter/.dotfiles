"""
TinyLlama model implementation.
"""
from typing import Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from .base import LLMInterface

class TinyLlamaModel(LLMInterface):
    """TinyLlama implementation of the LLM interface."""
    
    def __init__(self):
        self.model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        
    def load_model(self) -> None:
        """Load the TinyLlama model and tokenizer."""
        if self.model is not None:
            return  # Model already loaded
            
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,  # Use float32 for CPU
            device_map=self.device
        )
        
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )
    
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """Generate a response using TinyLlama."""
        if self.pipeline is None:
            self.load_model()
            
        # Format prompt for chat
        formatted_prompt = f"<|system|>You are a helpful AI assistant.</s><|user|>{prompt}</s><|assistant|>"
        
        # Generate response
        response = self.pipeline(
            formatted_prompt,
            max_length=max_length or 200,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )[0]["generated_text"]
        
        # Extract just the assistant's response
        try:
            response = response.split("<|assistant|>")[1].strip()
            if "</s>" in response:
                response = response.split("</s>")[0].strip()
        except IndexError:
            response = "I apologize, but I couldn't generate a proper response."
            
        return response 