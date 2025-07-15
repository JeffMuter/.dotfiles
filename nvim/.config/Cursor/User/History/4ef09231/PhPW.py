"""
SignalWire client implementation for AI phone calls.
"""
import os
from dataclasses import asdict
from typing import Optional
import requests
from menu.cli import CallDetails

class SignalWireClient:
    """Client for interacting with SignalWire's LAML API."""
    
    # Available voice options (Amazon Polly Neural voices)
    AVAILABLE_VOICES = {
        'female': {
            'en-US': 'joanna',
            'en-GB': 'amy',
            'en-AU': 'olivia'
        },
        'male': {
            'en-US': 'matthew',
            'en-GB': 'brian',
            'en-AU': 'russell'
        }
    }
    
    def __init__(self, api_key: Optional[str] = None, voice_gender: str = 'female', voice_locale: str = 'en-US'):
        """Initialize the SignalWire client.
        
        Args:
            api_key: SignalWire API key. If not provided, will try to get from environment.
            voice_gender: 'male' or 'female' (default: 'female')
            voice_locale: 'en-US', 'en-GB', or 'en-AU' (default: 'en-US')
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
        
        # Set voice preferences
        if voice_gender not in self.AVAILABLE_VOICES:
            raise ValueError(f"voice_gender must be one of: {list(self.AVAILABLE_VOICES.keys())}")
        if voice_locale not in self.AVAILABLE_VOICES[voice_gender]:
            raise ValueError(f"voice_locale must be one of: {list(self.AVAILABLE_VOICES[voice_gender].keys())}")
            
        self.voice_name = self.AVAILABLE_VOICES[voice_gender][voice_locale]
        
        # SignalWire LAML API base URL
        self.base_url = f"https://saorsadev.signalwire.com/api/laml/2010-04-01/Accounts/{self.project_id}"
        
        # Create a default LAML bin for AI conversation with neural voice
        self.default_laml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="amazon:neural:{voice}">
        <break time="500ms"/>
        {prompt}
    </Say>
</Response>"""
        
    def make_call(self, call_details: CallDetails) -> dict:
        """Initiate a phone call using SignalWire LAML API.
        
        Args:
            call_details: CallDetails object containing call information
            
        Returns:
            dict: Response from SignalWire API
        """
        # Create the prompt for the AI
        prompt = self._create_prompt(call_details)
        
        # Create LAML with the prompt and voice settings
        laml = self.default_laml.format(
            prompt=prompt,
            voice=self.voice_name.lower()  # Amazon voices need to be lowercase
        )
        
        # Convert call details to API format
        payload = {
            'To': call_details.phone_number,
            'From': self.phone_number,
            'Twiml': laml
        }
        
        # Make API request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/Calls",
                data=payload,
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
        prompt = f"""Hello, this is {call_details.caller_name} calling {call_details.contact_name}.
{call_details.objective}"""

        if call_details.additional_context:
            prompt += f". {call_details.additional_context}"
            
        return prompt 