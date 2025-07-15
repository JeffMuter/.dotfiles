#!/usr/bin/env python3
"""
CallHiss - AI-powered phone call assistant
A CLI tool that makes phone calls with AI agents to deliver messages.
"""

import os
import sys
import argparse
from flask import Flask, request, Response
from signalwire.rest import Client as signalwire_client
from signalwire.voice_response import VoiceResponse
import threading
import time
import signal
import json
from urllib.parse import urlencode

class CallHiss:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.server_thread = None
        self.port = int(os.getenv('PORT', 3000))
        self.host = os.getenv('HOST_APP', f'http://localhost:{self.port}')
        
        # SignalWire credentials - ensure these are set as environment variables
        self.space_url = os.getenv('SPACE_URL')
        self.project_id = os.getenv('PROJECT_ID')
        self.api_token = os.getenv('API_TOKEN')
        
        if not all([self.space_url, self.project_id, self.api_token]):
            print("❌ Error: Missing required environment variables:")
            print("   Please set: SPACE_URL, PROJECT_ID, API_TOKEN")
            sys.exit(1)
            
        self.client = signalwire_client(
            self.project_id, 
            self.api_token, 
            signalwire_space_url=self.space_url
        )
        
    def setup_routes(self):
        """Setup Flask routes for handling SignalWire webhooks"""
        
        @self.app.route('/ai-agent', methods=['POST'])
        def ai_agent():
            """Main AI agent endpoint that handles the call"""
            response = VoiceResponse()
            connect = response.connect()
            
            # Get the call context from the request
            call_context = request.form.get('call_context', '{}')
            context_data = json.loads(call_context) if call_context else {}
            
            user_prompt = context_data.get('user_prompt', '')
            caller_context = context_data.get('caller_context', '')
            
            # Initialize AI agent
            agent = connect.ai(voice="en-US-Neural2-D")
            agent.set_post_prompt_url(f"{self.host}/summary")
            
            # Create the AI prompt based on user's request
            ai_prompt = f"""You are an AI assistant making a phone call on behalf of someone.
            
            Context: {user_prompt}
            
            Your job is to:
            1. Greet the person who answers politely
            2. Deliver the message exactly as requested
            3. Handle any questions or responses naturally
            4. Keep the conversation brief and focused on the objective
            5. Say goodbye politely and end the call
            
            Additional context about the caller: {caller_context}
            
            Be natural, friendly, and complete the objective efficiently. 
            If they ask questions you can't answer, politely explain you're calling on behalf of someone else.
            Always end the conversation politely and hang up when the objective is complete.
            """
            
            agent.prompt({"confidence": 0.6, "frequency_penalty": 0.3}, ai_prompt)
            
            # Post-prompt for call summary
            agent.post_prompt("""Return a JSON object with the call results:
            {"call_completed": true/false, "response_received": "RESPONSE", "notes": "NOTES"}""")
            
            print(f"🤖 AI agent handling call with prompt: {user_prompt[:50]}...")
            return Response(str(response), mimetype='text/xml')
        
        @self.app.route('/summary', methods=['POST'])
        def summary():
            """Receive call summary from AI agent"""
            caller_id = request.form.get('caller_id_number', 'Unknown')
            print(f"\n📞 Call completed to: {caller_id}")
            
            if hasattr(request.form, 'post_prompt_data'):
                try:
                    summary_data = json.loads(request.form.get('post_prompt_data', '{}'))
                    print(f"📋 Call Summary: {summary_data}")
                except:
                    print(f"📋 Raw Summary: {request.form.get('post_prompt_data', 'No summary available')}")
            
            return Response('OK', status=200)
    
    def start_server(self):
        """Start the Flask server in a separate thread"""
        def run_server():
            self.app.run(host='0.0.0.0', port=self.port, debug=False)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(2)  # Give server time to start
        print(f"🌐 Webhook server started on {self.host}")
    
    def make_call(self, phone_number: str, user_prompt: str, caller_context: str = ""):
        """Initiate the AI-powered phone call"""
        print(f"📞 Initiating call to {phone_number}...")
        print(f"🎯 Objective: {user_prompt}")
        
        # Prepare call context as URL parameters
        call_context = {
            'user_prompt': user_prompt,
            'caller_context': caller_context
        }
        
        # Encode context as URL parameters
        context_params = urlencode({'call_context': json.dumps(call_context)})
        webhook_url = f"{self.host}/ai-agent?{context_params}"
        
        try:
            call = self.client.calls.create(
                url=webhook_url,
                to=phone_number,
                from_=os.getenv('FROM_NUMBER'),  # Your SignalWire phone number
                method='POST'
            )
            
            print(f"✅ Call initiated successfully!")
            print(f"📋 Call SID: {call.sid}")
            print(f"📊 Call Status: {call.status}")
            
            return call
            
        except Exception as e:
            print(f"❌ Failed to initiate call: {str(e)}")
            return None
    
    def run_cli(self):
        """Main CLI interface"""
        print("🎵 CallHiss - AI Phone Call Assistant")
        print("=" * 40)
        
        # Start the webhook server
        self.start_server()
        
        try:
            while True:
                print("\n💭 What would you like the AI to say on the call?")
                print("   (Example: 'call this person, tell them happy birthday! Its my mom, and tell her its from James!')")
                print("\n📝 Enter your prompt (or 'quit' to exit):")
                
                user_prompt = input("> ").strip()
                
                if user_prompt.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_prompt:
                    print("❌ Please enter a prompt")
                    continue
                
                print("\n📞 Enter the phone number to call (include country code, e.g., +1234567890):")
                phone_number = input("> ").strip()
                
                if not phone_number:
                    print("❌ Please enter a valid phone number")
                    continue
                
                # Optional: Ask for additional context
                print("\n🔍 Any additional context about yourself? (optional, press Enter to skip):")
                caller_context = input("> ").strip()
                
                # Confirm before making the call
                print(f"\n🎯 Ready to call {phone_number}")
                print(f"📝 Message: {user_prompt}")
                if caller_context:
                    print(f"👤 Context: {caller_context}")
                
                confirm = input("\n✅ Proceed with call? (y/N): ").strip().lower()
                
                if confirm == 'y':
                    call = self.make_call(phone_number, user_prompt, caller_context)
                    if call:
                        print("\n🔄 Call in progress... Check the summary above when complete.")
                        print("   You can start another call or type 'quit' to exit.")
                else:
                    print("❌ Call cancelled")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="CallHiss - AI-powered phone call assistant")
    parser.add_argument("--version", action="version", version="CallHiss 1.0.0")
    args = parser.parse_args()
    
    # Check environment variables
    required_vars = ['SPACE_URL', 'PROJECT_ID', 'API_TOKEN', 'FROM_NUMBER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   export {var}=your_value_here")
        print("\n📚 Please check the README for setup instructions.")
        sys.exit(1)
    
    call_hiss = CallHiss()
    call_hiss.run_cli()

if __name__ == "__main__":
    main() 