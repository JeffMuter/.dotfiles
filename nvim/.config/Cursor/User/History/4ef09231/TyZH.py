"""
SignalWire client implementation for AI phone calls.
"""
import os
from dataclasses import asdict
from typing import Optional, Dict, Any, List
import requests
from menu.cli import CallDetails

class SignalWireClient:
    """Client for interacting with SignalWire's AI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the SignalWire client.
        
        Args:
            api_key: SignalWire API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.environ.get("SIGNALWIRE_API_KEY")
        if not self.api_key:
            raise ValueError("SignalWire API key must be provided either directly or via SIGNALWIRE_API_KEY environment variable")
        
        # Get SignalWire phone number from environment
        self.phone_number = os.environ.get("SIGNALWIRE_PHONE_NUMBER")
        if not self.phone_number:
            raise ValueError("SIGNALWIRE_PHONE_NUMBER environment variable must be set with your SignalWire phone number")
        
        # Add + prefix if not present
        if not self.phone_number.startswith("+"):
            self.phone_number = f"+{self.phone_number}"
        
        # Get project ID from environment
        self.project_id = os.environ.get("SIGNALWIRE_PROJECT_ID")
        if not self.project_id:
            raise ValueError("SIGNALWIRE_PROJECT_ID environment variable must be set")
        
        # SignalWire AI API base URL
        self.base_url = f"https://saorsadev.signalwire.com/api/fabric/resources/ai_agents"
    
    def _create_ai_configuration(self, call_details: CallDetails) -> Dict[str, Any]:
        """Create the AI configuration for the call.
        
        Args:
            call_details: CallDetails object containing call information
            
        Returns:
            dict: AI configuration for the request
        """
        prompt_text = self._create_prompt(call_details)
        
        # Required configuration
        config = {
            "name": f"Call to {call_details.contact_name}",  # Required field
            "prompt": {
                "text": prompt_text,  # Required field
                "temperature": 0.7,
                "top_p": 0.8,
                "confidence": 0.8,
                "presence_penalty": 0.0,
                "frequency_penalty": 0.0
            },
            "post_prompt": {
                "text": "",  # Empty as requested to not record
                "temperature": 0.7,
                "top_p": 0.8
            },
            "params": {
                "wait_for_user": True,  # Wait for user to speak first
                "save_conversation": False,  # Don't save the conversation
                "languages_enabled": False,  # Single language only
                "end_of_speech_timeout": 1000,  # 1 second of silence to detect end of speech
                "energy_level": 50,  # Default energy level for voice detection
                "debug_webhook_level": 0,  # No debugging
                "verbose_logs": False
            },
            "hints": [],  # No specific hints
            "languages": [
                {
                    "name": "English",
                    "code": "en-US"
                }
            ]
        }
        
        return config

    def make_call(self, call_details: CallDetails) -> dict:
        """Initiate an AI phone call using SignalWire AI API.
        
        Args:
            call_details: CallDetails object containing call information
            
        Returns:
            dict: Response from SignalWire API
        """
        # Get AI configuration
        ai_config = self._create_ai_configuration(call_details)
        
        # Create call payload with correct structure
        payload = {
            'number': call_details.phone_number,
            'from_number': self.phone_number,
            'ai_agent': ai_config  # Changed from ai_config to ai_agent to match schema
        }
        
        # Make API request
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}",
                json=payload,
                headers=headers,
                auth=(self.project_id, self.api_key)
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to initiate SignalWire call: {str(e)}")
    
    def _create_prompt(self, call_details: CallDetails) -> str:
        """Create the AI prompt from call details.
        
        Args:
            call_details: CallDetails object containing call information
            
        Returns:
            str: Formatted prompt for the AI
        """
        prompt = f"""You are {call_details.caller_name}, and you are calling {call_details.contact_name}.
Your objective is: {call_details.objective}"""

        if call_details.additional_context:
            prompt += f"\n\nAdditional context: {call_details.additional_context}"
            
        return prompt 