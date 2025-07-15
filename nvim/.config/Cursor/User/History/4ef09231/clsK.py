"""
Fixed SignalWire client implementation for AI phone calls.
This version uses proper LaML structure like the working Node.js version.
"""
import os
import requests
from urllib.parse import urlencode
from typing import Optional

class SignalWireClient:
    """Client for interacting with SignalWire's AI API."""
    
    def __init__(self, api_key=None):
        """Initialize the SignalWire client."""
        self.api_key = api_key or os.environ.get("SIGNALWIRE_API_KEY")
        if not self.api_key:
            raise ValueError("SignalWire API key must be provided either directly or via SIGNALWIRE_API_KEY environment variable")
        
        self.phone_number = os.environ.get("SIGNALWIRE_PHONE_NUMBER")
        if not self.phone_number:
            raise ValueError("SIGNALWIRE_PHONE_NUMBER environment variable must be set")
        
        if not self.phone_number.startswith("+"):
            self.phone_number = f"+{self.phone_number}"
        
        self.project_id = os.environ.get("SIGNALWIRE_PROJECT_ID")
        if not self.project_id:
            raise ValueError("SIGNALWIRE_PROJECT_ID environment variable must be set")
        
        self.space_name = os.environ.get("SIGNALWIRE_SPACE_NAME")
        if not self.space_name:
            raise ValueError("SIGNALWIRE_SPACE_NAME environment variable must be set")
        
        self.base_url = f"https://{self.space_name}.signalwire.com"
        self.voice_url = f"{self.base_url}/api/laml/2010-04-01/Accounts/{self.project_id}/Calls"
    
    def initiate_ai_call(self, to_number: Optional[str] = None) -> dict:
        """Initiate an AI call using proper LaML structure.
        
        Args:
            to_number: Optional override for the target phone number
            
        Returns:
            dict: API response containing call details
        """
        target_number = to_number or os.environ.get("TARGET_PHONE_NUMBER")
        if not target_number:
            raise ValueError("Either to_number must be provided or TARGET_PHONE_NUMBER environment variable must be set")
            
        if not target_number.startswith("+"):
            target_number = f"+{target_number}"
        
        # Get AI prompt from environment
        ai_prompt = os.environ.get('AI_PROMPT', 'You are a helpful AI assistant making a phone call.')
        
        # Use the same LaML structure as the working Node.js version
        # The key difference: use Connect + AI instead of direct AI element
        laml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <AI voice="{os.environ.get('SIGNALWIRE_VOICE_GENDER', 'en-US')}-Neural2-D">
            <Prompt confidence="0.4" frequencyPenalty="0.3">
{ai_prompt}

Remember to:
1. Introduce yourself clearly at the start
2. State your purpose for calling
3. Speak naturally and professionally
4. Listen and respond appropriately
5. Keep the conversation focused on the objective
6. Be sure to hang up the call at the end of every conversation
            </Prompt>
        </AI>
    </Connect>
</Response>'''
        
        # Payload for initiating the call
        payload = {
            'To': target_number,
            'From': self.phone_number,
            'Twiml': laml,  # Use the corrected LaML structure
        }
        
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
            
            print(f"Call initiated - Status: {response.status_code}")
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Error response: {e.response.text}")
            raise RuntimeError(f"Failed to initiate SignalWire call: {str(e)}")

# Example usage
if __name__ == "__main__":
    client = SignalWireClient()
    result = client.initiate_ai_call()
    print("🤖 Call initiated successfully!")
    print("Response Details:")
    for key, value in result.items():
        print(f"{key}: {value}")