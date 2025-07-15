"""
SignalWire client implementation for AI phone calls.
"""
import os
from dataclasses import asdict
from typing import Optional, Dict, Any, List
import requests
from urllib.parse import urlencode
import base64
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
        
        # SignalWire base URLs
        self.space_name = os.environ.get("SIGNALWIRE_SPACE_NAME")
        if not self.space_name:
            raise ValueError("SIGNALWIRE_SPACE_NAME environment variable must be set")
            
        self.base_url = f"https://{self.space_name}.signalwire.com"
        self.ai_agent_url = f"{self.base_url}/api/fabric/resources/ai_agents"
        self.voice_url = f"{self.base_url}/api/calling/calls"

    def _create_ai_configuration(self, call_details: CallDetails) -> Dict[str, Any]:
        """Create the AI configuration for the call.
        
        Args:
            call_details: CallDetails object containing call information
            
        Returns:
            dict: AI configuration for the request
        """
        prompt_text = self._create_prompt(call_details)
        
        config = {
            "name": call_details.caller_name,
            "prompt": {
                "text": prompt_text,
                "temperature": 0.7,
                "confidence": 0.8
            },
            "post_prompt": {
                "text": ""  # No summary needed
            },
            "params": {
                "wait_for_user": False,  # AI initiates the conversation
                "ai_volume": 10,
                "direction": ["outbound"],
                "save_conversation": False
            },
            "pronounce": [],
            "hints": [
                f"You are {call_details.caller_name} calling {call_details.contact_name}",
                f"Your objective is: {call_details.objective}"
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
        # First, create the AI agent
        ai_config = self._create_ai_configuration(call_details)
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            # Step 1: Create AI Agent
            agent_response = requests.post(
                self.ai_agent_url,
                json=ai_config,
                headers=headers,
                auth=(self.project_id, self.api_key)
            )
            agent_response.raise_for_status()
            agent_data = agent_response.json()
            agent_id = agent_data.get('id')
            
            if not agent_id:
                raise RuntimeError("Failed to get AI agent ID from response")
            
            # Step 2: Initiate the call with the AI agent
            call_payload = {
                "to": call_details.phone_number,
                "from": self.phone_number,
                "ai_agent_id": agent_id
            }
            
            call_response = requests.post(
                self.voice_url,
                json=call_payload,
                headers=headers,
                auth=(self.project_id, self.api_key)
            )
            call_response.raise_for_status()
            return call_response.json()
            
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

    def make_simple_ai_call(self, to_number: str, prompt: str) -> dict:
        """Make a simple AI call directly using the Calling API.
        
        Args:
            to_number: The phone number to call (E.164 format)
            prompt: The AI agent's instructions/prompt
            
        Returns:
            dict: API response containing call details
        """
        # Create simple AI configuration
        ai_config = {
            "prompt": {
                "text": prompt,
                "temperature": 0.7,
                "confidence": 0.8
            },
            "params": {
                "wait_for_user": False,
                "ai_volume": 10
            }
        }
        
        # Create call payload
        payload = {
            "to": to_number,
            "from": self.phone_number,
            "ai": ai_config
        }
        
        # Headers
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(
                self.voice_url,
                json=payload,
                headers=headers,
                auth=(self.project_id, self.api_key)
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to initiate SignalWire call: {str(e)}")

    @staticmethod
    def create_ai_webhook_response(prompt: str, voice: str = "en-US-Neural2-D") -> str:
        """Generate the XML response for the webhook that creates an AI agent.
        This is what your webhook endpoint should return.
        
        Args:
            prompt: The AI agent's instructions
            voice: Voice to use for TTS
            
        Returns:
            str: XML response for SignalWire
        """
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <AI voice="{voice}">
            <Prompt>{prompt}</Prompt>
        </AI>
    </Connect>
</Response>''' 