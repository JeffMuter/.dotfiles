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
import anthropic

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
        
        # Anthropic AI setup
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.anthropic_client = None
        if self.anthropic_api_key and self.anthropic_api_key != 'your_anthropic_api_key_here':
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
                print("🤖 Anthropic AI enabled for intelligent responses")
            except Exception as e:
                print(f"⚠️  Anthropic AI setup failed: {e}")
                print("   Falling back to simple keyword responses")
        else:
            print("⚠️  No Anthropic API key found. Using simple keyword responses.")
            print("   Add ANTHROPIC_API_KEY to config.env for AI-powered conversations")
        
        if not all([self.space_url, self.project_id, self.api_token]):
            print("❌ Error: Missing required environment variables:")
            print("   Please set: SPACE_URL, PROJECT_ID, API_TOKEN")
            print("   Run: source config.env")
            sys.exit(1)
        
        # Fix space URL format
        if not self.space_url.endswith('.signalwire.com'):
            self.space_url = f"{self.space_url}.signalwire.com"
            
        # Test credentials before proceeding
        if not self._test_credentials():
            print("❌ Authentication failed! Please run the credential verification tool:")
            print("   python verify_credentials.py")
            sys.exit(1)
            
        self.client = signalwire_client(
            self.project_id, 
            self.api_token, 
            signalwire_space_url=self.space_url
        )
        
        # Store conversation history for context
        self.conversation_history = {}
        
    def _test_credentials(self):
        """Test SignalWire credentials before starting the application"""
        try:
            print("🔐 Verifying SignalWire credentials...")
            client = signalwire_client(
                self.project_id, 
                self.api_token, 
                signalwire_space_url=self.space_url
            )
            
            # Test with a simple API call
            account = client.api.account.fetch()
            print(f"✅ Authentication successful! Account: {account.sid}")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            
            if "401" in str(e) or "Unauthorized" in str(e):
                print("\n🔍 This is a 401 Unauthorized error. Common causes:")
                print("   1. Incorrect API Token")
                print("   2. Incorrect Project ID")
                print("   3. Credentials from wrong SignalWire Space")
                print("   4. Expired or revoked API Token")
                print("\n🔧 To fix:")
                print("   1. Go to https://signalwire.com/signin")
                print(f"   2. Select your space: {self.space_url.replace('.signalwire.com', '')}")
                print("   3. Go to API section")
                print("   4. Copy the correct Project ID and API Token")
                print("   5. Update config.env")
                print("   6. Run: source config.env")
                print("\n🛠️  Or run the verification tool: python verify_credentials.py")
            
            return False
        
    def setup_routes(self):
        """Setup Flask routes for handling SignalWire webhooks"""
        
        @self.app.route('/ai-agent', methods=['POST'])
        def ai_agent():
            """Main AI agent endpoint that handles the call"""
            response = VoiceResponse()
            
            # Get the call context from URL parameters
            call_context = request.args.get('call_context', '{}')
            context_data = json.loads(call_context) if call_context else {}
            
            user_prompt = context_data.get('user_prompt', '')
            caller_context = context_data.get('caller_context', '')
            
            # Check if this is a response from the user (speech recognition result)
            speech_result = request.form.get('SpeechResult', '')
            confidence = request.form.get('Confidence', '')
            
            if speech_result:
                # User has spoken - process their response
                print(f"👤 User said: '{speech_result}' (confidence: {confidence})")
                
                # Simple conversation logic
                speech_lower = speech_result.lower()
                
                if 'yes' in speech_lower or 'yeah' in speech_lower:
                    response.say("Great! I can hear you clearly too. This confirms our AI calling system is working perfectly.")
                    response.say("Is there anything else you'd like to test or should I end the call?")
                    # Listen for another response
                    response.gather(
                        input='speech',
                        timeout=10,
                        speech_timeout='auto',
                        action=f'{self.host}/ai-agent?' + urlencode({'call_context': json.dumps(context_data)})
                    )
                elif 'no' in speech_lower:
                    response.say("I'm sorry to hear that. Let me try speaking louder and clearer.")
                    response.say("Can you hear me better now?")
                    response.gather(
                        input='speech',
                        timeout=10,
                        speech_timeout='auto', 
                        action=f'{self.host}/ai-agent?' + urlencode({'call_context': json.dumps(context_data)})
                    )
                elif 'bye' in speech_lower or 'goodbye' in speech_lower or 'end' in speech_lower:
                    response.say("Thank you for testing the CallHiss AI system! Goodbye!")
                    response.hangup()
                elif 'hello' in speech_lower or 'hi' in speech_lower:
                    response.say("Hello! Nice to hear from you. The AI conversation system is working well!")
                    response.say("Try saying something else and I'll respond appropriately.")
                    response.gather(
                        input='speech',
                        timeout=15,
                        speech_timeout='auto',
                        action=f'{self.host}/ai-agent?' + urlencode({'call_context': json.dumps(context_data)})
                    )
                else:
                    # Generic response to keep conversation going
                    response.say(f"I heard you say: {speech_result}")
                    response.say("This shows our speech recognition is working. Try saying 'yes', 'no', or 'goodbye' to test different responses.")
                    response.gather(
                        input='speech',
                        timeout=15,
                        speech_timeout='auto',
                        action=f'{self.host}/ai-agent?' + urlencode({'call_context': json.dumps(context_data)})
                    )
            else:
                # Initial call - start the conversation
                if user_prompt:
                    response.say(f"Hello! {user_prompt}")
                else:
                    response.say("Hello! This is the CallHiss AI assistant. I'm calling to have a conversation with you.")
                
                response.say("Can you hear me clearly? Please say yes or no.")
                
                # Use Gather to listen for user response
                response.gather(
                    input='speech',
                    timeout=10,
                    speech_timeout='auto',
                    action=f'{self.host}/ai-agent?' + urlencode({'call_context': json.dumps(context_data)})
                )
                
                # Fallback if no response
                response.say("I didn't hear a response. Let me try again.")
                response.say("Please say something so I know you can hear me.")
                response.gather(
                    input='speech',
                    timeout=15,
                    speech_timeout='auto',
                    action=f'{self.host}/ai-agent?' + urlencode({'call_context': json.dumps(context_data)})
                )
                
                # Final fallback
                response.say("I still can't hear you. I'll end the call now. Please try calling back.")
                response.hangup()
            
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
            
            # Provide specific guidance for common errors
            if "401" in str(e):
                print("🔍 This looks like an authentication error.")
                print("   Run: python verify_credentials.py")
            elif "from" in str(e).lower():
                print("🔍 This might be an issue with your FROM_NUMBER.")
                print("   Check that FROM_NUMBER in config.env matches a number in your account.")
            
            return None
    
    def generate_ai_response(self, user_speech: str, user_prompt: str, caller_context: str, call_sid: str = None):
        """Generate AI response using Claude based on user speech and context"""
        if not self.anthropic_client:
            # Fallback to simple responses if no AI available
            return self._generate_simple_response(user_speech)
        
        try:
            # Get or initialize conversation history for this call
            if call_sid not in self.conversation_history:
                self.conversation_history[call_sid] = []
            
            # Add user speech to history
            self.conversation_history[call_sid].append(f"Human: {user_speech}")
            
            # Create conversation context
            history_context = "\n".join(self.conversation_history[call_sid][-5:])  # Last 5 exchanges
            
            # Create the AI prompt
            system_prompt = f"""You are an AI assistant making a phone call. You are speaking directly to someone on the phone right now.

Original call objective: {user_prompt}
Additional context: {caller_context}

Guidelines:
1. Be natural and conversational - you're speaking, not writing
2. Keep responses brief (1-2 sentences max) since this is a phone call
3. Stay focused on the call objective when appropriate
4. Be helpful and friendly
5. If someone wants to end the call, politely agree
6. Don't mention that you're an AI unless directly asked

Recent conversation:
{history_context}

The person just said: "{user_speech}"

Respond naturally as if you're speaking to them on the phone right now. Keep it brief and conversational."""

            # Get AI response from Claude
            message = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",  # Fast model for real-time calls
                max_tokens=150,  # Keep responses brief for phone calls
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"Please respond to: {user_speech}"}
                ]
            )
            
            ai_response = message.content[0].text.strip()
            
            # Add AI response to history
            self.conversation_history[call_sid].append(f"Assistant: {ai_response}")
            
            print(f"🤖 AI generated response: {ai_response}")
            return ai_response
            
        except Exception as e:
            print(f"❌ AI response generation failed: {e}")
            return self._generate_simple_response(user_speech)
    
    def _generate_simple_response(self, user_speech: str):
        """Fallback simple response generation when AI is not available"""
        speech_lower = user_speech.lower()
        
        if 'yes' in speech_lower or 'yeah' in speech_lower:
            return "Great! I can hear you clearly too. This confirms our calling system is working perfectly."
        elif 'no' in speech_lower:
            return "I'm sorry to hear that. Let me try speaking louder and clearer. Can you hear me better now?"
        elif 'bye' in speech_lower or 'goodbye' in speech_lower or 'end' in speech_lower:
            return "Thank you for testing the CallHiss AI system! Goodbye!"
        elif 'hello' in speech_lower or 'hi' in speech_lower:
            return "Hello! Nice to hear from you. The conversation system is working well!"
        else:
            return f"I heard you say: {user_speech}. This shows our speech recognition is working perfectly!"
    
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