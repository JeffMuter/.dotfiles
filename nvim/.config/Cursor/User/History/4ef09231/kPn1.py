"""
Fixed SignalWire client implementation for AI phone calls.
This version properly uses webhook URLs instead of sending LaML directly.
"""

import os
import time
import requests
from urllib.parse import urlencode
from typing import Optional

class SignalWireClient:
    """Client for interacting with SignalWire's AI API using webhooks."""
    
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
        
        self.webhook_url = os.environ.get("WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError("WEBHOOK_URL environment variable must be set (e.g., https://your-ngrok-url.ngrok.io/ai-agent)")
        
        self.base_url = f"https://{self.space_name}.signalwire.com"
        self.voice_url = f"{self.base_url}/api/laml/2010-04-01/Accounts/{self.project_id}/Calls"
        
        # Initialize rate limiting variables
        self.last_call_time = 0
        self.min_call_interval = 1.0  # Minimum 1 second between calls
    
    def _enforce_rate_limit(self):
        """Enforce rate limiting by waiting if needed."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.min_call_interval:
            wait_time = self.min_call_interval - time_since_last_call
            time.sleep(wait_time)
        
        self.last_call_time = time.time()
    
    def _check_call_status(self, call_sid: str, max_retries: int = 10, delay: int = 2) -> dict:
        """Check the status of a call by its SID."""
        status_url = f"{self.voice_url}/{call_sid}"
        headers = {'Accept': 'application/json'}
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    status_url,
                    headers=headers,
                    auth=(self.project_id, self.api_key)
                )
                response.raise_for_status()
                status_data = response.json()
                
                # Print status updates
                if attempt == 0 or status_data.get('status') != getattr(self, '_last_status', None):
                    print(f"📞 Call Status: {status_data.get('status')}")
                    if status_data.get('start_time'):
                        print(f"⏰ Start Time: {status_data.get('start_time')}")
                    if status_data.get('duration'):
                        print(f"⏱️ Duration: {status_data.get('duration')}s")
                    self._last_status = status_data.get('status')
                
                # If the call has moved beyond queued state
                if status_data.get('status') not in ['queued', None]:
                    return status_data
                
                time.sleep(delay)
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Error checking call status: {str(e)}")
                time.sleep(delay)
        
        return {'status': 'unknown', 'error': 'Max retries reached while checking call status'}

    def initiate_ai_call(self, to_number: Optional[str] = None) -> dict:
        """
        Initiate an AI call using webhook URL (the correct approach).
        
        Args:
            to_number: Optional override for the target phone number
            
        Returns:
            dict: API response containing call details
        """
        # Enforce rate limiting before making the call
        self._enforce_rate_limit()
        
        target_number = to_number or os.environ.get("TARGET_PHONE_NUMBER")
        if not target_number:
            raise ValueError("Either to_number must be provided or TARGET_PHONE_NUMBER environment variable must be set")
            
        if not target_number.startswith("+"):
            target_number = f"+{target_number}"
        
        print(f"🚀 Initiating AI call from {self.phone_number} to {target_number}")
        print(f"🔗 Using webhook URL: {self.webhook_url}")
        
        # Payload for initiating the call - NO LaML, just webhook URL
        payload = {
            'To': target_number,
            'From': self.phone_number,
            'Url': self.webhook_url,  # Point to your webhook server
            'Method': 'POST',
            # Note: NO 'Twiml' parameter! SignalWire will call our webhook for LaML
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
            
            print(f"📡 Call request sent - Status: {response.status_code}")
            response.raise_for_status()
            initial_response = response.json()
            
            # Check if we got a call SID
            if 'sid' in initial_response:
                print(f"📋 Call SID: {initial_response['sid']}")
                
                # Monitor the call status
                status_response = self._check_call_status(initial_response['sid'])
                
                if status_response.get('status') == 'failed':
                    print("\n❌ Call failed. This might be due to:")
                    print("   1. Webhook URL not accessible")
                    print("   2. Trial account limitations")
                    print("   3. Numbers not properly verified")
                    print("   4. SignalWire service issues")
                    print(f"   5. Check that {self.webhook_url} is running and accessible")
                elif status_response.get('status') in ['completed', 'busy', 'no-answer']:
                    print(f"✅ Call completed with status: {status_response.get('status')}")
                
                return status_response
            
            return initial_response
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Error response: {e.response.text}")
            raise RuntimeError(f"Failed to initiate SignalWire call: {str(e)}")

    def test_webhook_connectivity(self) -> bool:
        """Test if the webhook URL is accessible."""
        try:
            response = requests.get(f"{self.webhook_url.replace('/ai-agent', '/health')}", timeout=5)
            if response.status_code == 200:
                print(f"✅ Webhook server is accessible at {self.webhook_url}")
                return True
            else:
                print(f"⚠️ Webhook server responded with status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Webhook server is not accessible: {str(e)}")
            print("   Make sure your webhook server is running and exposed via ngrok or similar")
            return False

# Example usage
if __name__ == "__main__":
    # Test the client
    client = SignalWireClient()
    
    # First, test webhook connectivity
    if client.test_webhook_connectivity():
        print("\n🚀 Webhook is accessible, initiating call...")
        result = client.initiate_ai_call()
        print("\n📊 Final Call Status:")
        for key, value in result.items():
            print(f"   {key}: {value}")
    else:
        print("\n❌ Cannot initiate call - webhook server is not accessible")
        print("   Please start your webhook server and expose it via ngrok")