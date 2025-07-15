"""
TinyLlama model implementation.
"""
from typing import Optional
import torch
from rich.progress import Progress, SpinnerColumn, TextColumn
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
        
        # Adjust loading based on device
        if self.device == "cuda":
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto"
            )
        else:
            # CPU-specific loading
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            ).to(self.device)
        
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device if self.device == "cuda" else -1,  # -1 means CPU
            truncation=True,  # Enable truncation
            max_new_tokens=100  # Limit new tokens for faster generation
        )
    
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """Generate a response using TinyLlama."""
        if self.pipeline is None:
            self.load_model()
            
        # Format prompt for natural conversation
        system_prompt = """You are having a natural phone conversation. Respond in a casual, friendly way as if you're talking to someone on the phone. Keep your responses concise and conversational. Don't use formal structures, lists, or emojis. Speak in first person and respond directly to what the other person is saying."""
        
        formatted_prompt = f"<|system|>{system_prompt}</s><|user|>{prompt}</s><|assistant|>"
        
        # Show progress while generating
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Generating response...", total=None)
            
            # Generate response with parameters tuned for conversational style
            response = self.pipeline(
                formatted_prompt,
                max_length=max_length or 150,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.8,  # Slightly higher for more natural variation
                top_p=0.95,      # Slightly higher for more creative responses
                repetition_penalty=1.1,  # Reduced to allow more natural repetition in conversation
                truncation=True,
            )[0]["generated_text"]
        
        # Extract just the assistant's response
        try:
            response = response.split("<|assistant|>")[1].strip()
            if "</s>" in response:
                response = response.split("</s>")[0].strip()
        except IndexError:
            response = "I'm sorry, I'm having trouble responding right now."
            
        return response 