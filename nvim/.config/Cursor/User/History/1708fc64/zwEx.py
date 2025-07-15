"""
TinyLlama model implementation.
"""
from typing import Optional
import torch
import gc
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
            
        # Clear any existing cached memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
            
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            local_files_only=False,  # Allow downloading if not cached
        )
        
        # Adjust loading based on device
        if self.device == "cuda":
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto"
            )
        else:
            # CPU-specific optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
                offload_folder="offload_folder"  # Enable disk offloading
            ).to(self.device)
        
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device if self.device == "cuda" else -1,
            truncation=True,
            max_new_tokens=100
        )
        
    def unload_model(self) -> None:
        """Explicitly unload the model and free memory."""
        if self.model is not None:
            del self.pipeline
            del self.model
            del self.tokenizer
            self.pipeline = None
            self.model = None
            self.tokenizer = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
    
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """Generate a response using TinyLlama."""
        try:
            if self.pipeline is None:
                self.load_model()
            
            # Format prompt for natural conversation
            system_prompt = """You are having a real phone conversation. Respond ONLY with what you would actually say out loud on the phone.
- Speak in first person using natural, casual language
- Keep responses brief and conversational
- DO NOT describe actions, scenes, or narrate
- DO NOT use special characters or emojis
- Respond as if you are actually speaking on a phone call"""
            
            # Simplify the conversation prompt to be more direct
            conversation_prompt = prompt.strip()
            formatted_prompt = f"<|system|>{system_prompt}</s><|user|>{conversation_prompt}</s><|assistant|>"
            
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
                    max_length=max_length or 75,  # Even shorter for more natural dialogue
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7,  # Slightly lower for more focused responses
                    top_p=0.9,
                    repetition_penalty=1.2,  # Increased to avoid repetitive speech patterns
                    truncation=True,
                )[0]["generated_text"]
            
            # Extract just the assistant's response
            try:
                response = response.split("<|assistant|>")[1].strip()
                if "</s>" in response:
                    response = response.split("</s>")[0].strip()
                # Remove any remaining system-like text patterns
                response = response.replace("*", "").replace("[", "").replace("]", "")
                response = response.split("\n")[0]  # Take only the first line to keep it concise
            except IndexError:
                response = "Hey, I'm having trouble with the connection right now."
                
            # Cleanup after generation
            if self.device == "cpu":
                gc.collect()
                
            return response
            
        except RuntimeError as e:
            # Handle out-of-memory errors gracefully
            self.unload_model()
            return "Sorry, I'm having some technical difficulties. Can I call you back in a moment?" 