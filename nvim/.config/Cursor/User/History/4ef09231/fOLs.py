"""
Fixed SignalWire client implementation for AI phone calls.
This version properly implements the webhook pattern required by SignalWire.
"""
import os
from flask import Flask, request, Response
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
    
    def initiate_ai_call(self, webhook_url: str, to_number: Optional[str] = None) -> dict:
        """Initiate an AI call that will use a webhook to configure the agent.
        
        Args:
            webhook_url: Your webhook URL that will return LaML XML when called
            to_number: Optional override for the target phone number
            
        Returns:
            dict: API response containing call details
        """
        target_number = to_number or os.environ.get("TARGET_PHONE_NUMBER")
        if not target_number:
            raise ValueError("Either to_number must be provided or TARGET_PHONE_NUMBER environment variable must be set")
            
        if not target_number.startswith("+"):
            target_number = f"+{target_number}"
        
        # Simple payload - just tell SignalWire where to get instructions when call is answered
        payload = {
            'To': target_number,
            'From': self.phone_number,
            'Url': webhook_url,  # This MUST be your running webhook server
            'Method': 'POST'
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


# Flask webhook server to handle SignalWire callbacks
app = Flask(__name__)

# This is the critical webhook that SignalWire calls when the phone is answered
@app.route('/ai-webhook', methods=['POST'])
def ai_webhook():
    """Webhook that returns LaML XML to configure the AI agent."""
    
    # Get conversation state from the request if available
    conversation_state = request.form.get('ConversationState', '{}')
    call_sid = request.form.get('CallSid', '')
    
    # Get the prompt from environment or use default
    prompt = os.environ.get("AI_PROMPT", """
    You are a professional AI assistant making calls on behalf of a company.
    Your primary goals are:
    1. Introduce yourself clearly and state your purpose
    2. Engage in natural conversation while staying focused on the purpose
    3. Handle any questions or concerns professionally
    4. Maintain context throughout the conversation
    5. End the call politely when the purpose is achieved
    
    Remember to:
    - Always be polite and professional
    - Listen carefully to responses
    - Ask for clarification if needed
    - Keep track of important information shared
    - Summarize key points before ending
    """)
    
    # Create LaML XML response with enhanced AI configuration
    xml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <AI engine="openai" voice="en-US-Neural2-D" 
            endOfSpeechTimeout="1000"
            initialSilenceTimeout="5000"
            speechEndThreshold="1000"
            enhanced="true">
            <Prompt 
                confidence="0.6" 
                temperature="0.7"
                frequencyPenalty="0.3"
                presencePenalty="0.2"
                topP="0.9"
                maxTokens="150">
                {prompt}
            </Prompt>
            <Functions>
                <Function name="end_conversation">
                    <Parameter name="reason" type="string" />
                </Function>
                <Function name="set_follow_up">
                    <Parameter name="date" type="string" />
                    <Parameter name="notes" type="string" />
                </Function>
            </Functions>
        </AI>
    </Connect>
</Response>'''

    print("SignalWire called webhook - returning AI configuration")
    print(f"Call SID: {call_sid}")
    print(f"Conversation State: {conversation_state}")
    
    return Response(xml_response, mimetype='text/xml')

@app.route('/summary', methods=['POST'])
def summary():
    """Handle post-call summary from AI agent."""
    print("Call completed. Summary data:")
    print(f"Caller ID: {request.form.get('caller_id_number', 'Unknown')}")
    
    # Handle the post-prompt data
    if request.form.get('post_prompt_data'):
        print(f"AI Summary: {request.form.get('post_prompt_data')}")
    
    return "OK"

# Add a new endpoint to handle conversation summaries
@app.route('/conversation-summary', methods=['POST'])
def conversation_summary():
    """Handle post-conversation summary and analytics."""
    call_sid = request.form.get('CallSid', 'Unknown')
    summary = request.form.get('ConversationSummary', '')
    sentiment = request.form.get('ConversationSentiment', '')
    
    print(f"Call completed - SID: {call_sid}")
    print(f"Summary: {summary}")
    print(f"Sentiment: {sentiment}")
    
    # Here you could store the summary in a database
    # or trigger other post-call workflows
    
    return "OK"

# Example usage
if __name__ == "__main__":
    # For testing, you can run this Flask app and use ngrok to expose it
    # Then use the client to initiate calls
    
    # Example of how to make a call:
    # client = SignalWireClient()
    # webhook_url = "https://your-ngrok-url.ngrok.io/ai-webhook"
    # result = client.initiate_ai_call(webhook_url, "+1234567890")
    # print(result)
    
    app.run(debug=True, port=5000)