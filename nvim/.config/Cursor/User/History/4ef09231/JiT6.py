"""
SignalWire client implementation for AI phone calls.
"""
import os
from dataclasses import asdict
import requests
from urllib.parse import urlencode, quote
import base64
from typing import Optional

class SignalWireClient:
    """Client for interacting with SignalWire's AI API."""
    
    def __init__(self, api_key=None):
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
        # Use the correct Compatibility API endpoint
        self.voice_url = f"{self.base_url}/api/laml/2010-04-01/Accounts/{self.project_id}/Calls"
    
    def make_simple_ai_call(self, prompt: str, to_number: Optional[str] = None, 
                           voice: str = "en-US-Neural2-D", confidence: float = 0.4, 
                           frequency_penalty: float = 0.3, webhook_url: Optional[str] = None) -> dict:
        """Make a simple AI call directly using the LAML API.
        
        Args:
            prompt: The AI agent's instructions/prompt
            to_number: Optional override for the target phone number. If not provided,
                      will use TARGET_PHONE_NUMBER from environment.
            voice: Voice to use for the AI agent
            confidence: Confidence level for the AI agent
            frequency_penalty: Frequency penalty for the AI agent
            webhook_url: Optional webhook URL for handling the call
            
        Returns:
            dict: API response containing call details
        """
        # Get target number from args or environment
        target_number = to_number or os.environ.get("TARGET_PHONE_NUMBER")
        if not target_number:
            raise ValueError("Either to_number must be provided or TARGET_PHONE_NUMBER environment variable must be set")
            
        # Add + prefix if not present
        if not target_number.startswith("+"):
            target_number = f"+{target_number}"
        
        # Create LaML XML with AI agent configuration
        xml_script = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <AI engine="openai" voice="{voice}">
            <Prompt 
                confidence="{confidence}" 
                temperature="0.7"
                frequencyPenalty="{frequency_penalty}"
                endOfSpeechTimeout="500"
                initialSilenceTimeout="5000"
                digitalSilenceThresholdMs="500"
                speechThresholdMs="100"
                speechEndThresholdMs="1000"
                enhanced="true">
                {prompt}
                Start by introducing yourself and stating your purpose for calling.
            </Prompt>
        </AI>
    </Connect>
</Response>'''

        # Create call payload with URL-encoded XML
        payload = {
            'To': target_number,
            'From': self.phone_number,
            'Url': webhook_url or f"{self.base_url}/default-ai-response",  # Webhook URL must return the XML
            'Method': 'POST'  # Specify POST method for the webhook
        }
        
        # Add status callback if webhook provided
        if webhook_url:
            payload['StatusCallback'] = webhook_url
        
        # Headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(
                self.voice_url,
                data=urlencode(payload),
                headers=headers,
                auth=(self.project_id, self.api_key)
            )
            
            # Debug output
            print(f"Request URL: {self.voice_url}")
            print(f"Payload: {payload}")
            print(f"Response Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Error response: {e.response.text}")
            raise RuntimeError(f"Failed to initiate SignalWire call: {str(e)}")

    def make_ai_call_with_webhook(self, host_url: str, to_number: Optional[str] = None) -> dict:
        """Make an AI call using a webhook URL (similar to the Node.js version).
        
        Args:
            host_url: The base URL of your webhook server
            to_number: Optional override for the target phone number
            
        Returns:
            dict: API response containing call details
        """
        # Get target number from args or environment
        target_number = to_number or os.environ.get("TARGET_PHONE_NUMBER")
        if not target_number:
            raise ValueError("Either to_number must be provided or TARGET_PHONE_NUMBER environment variable must be set")
            
        # Add + prefix if not present
        if not target_number.startswith("+"):
            target_number = f"+{target_number}"
        
        # Create call payload pointing to webhook
        payload = {
            'To': target_number,
            'From': self.phone_number,
            'Url': f"{host_url}/"  # This should point to your webhook that returns LaML
        }
        
        # Headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(
                self.voice_url,
                data=payload,
                headers=headers,
                auth=(self.project_id, self.api_key)
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to initiate SignalWire call: {str(e)}")