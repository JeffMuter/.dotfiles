#!/usr/bin/env python3
"""
Test AI Call with Fixed SignalWire AI Implementation
"""

import os
import json
from urllib.parse import urlencode
from signalwire.rest import Client as signalwire_client

def test_ai_call():
    print("🎵 Testing AI Call with Fixed Implementation")
    print("=" * 45)
    
    # Load credentials
    space_url = os.getenv('SPACE_URL')
    project_id = os.getenv('PROJECT_ID') 
    api_token = os.getenv('API_TOKEN')
    from_number = os.getenv('FROM_NUMBER')
    host_app = os.getenv('HOST_APP')
    
    if not all([space_url, project_id, api_token, from_number, host_app]):
        print("❌ Missing environment variables. Run: source config.env")
        return
    
    if not space_url.endswith('.signalwire.com'):
        space_url = f"{space_url}.signalwire.com"
    
    print(f"🌐 Webhook URL: {host_app}")
    print(f"📞 From: {from_number}")
    
    # Get user input
    user_prompt = "Hi! This is a test call from the CallHiss AI assistant. I'm calling to verify that the AI agent is working properly. Can you hear me clearly? Please say yes if you can hear me."
    phone_number = "+16145572867"  # Your verified number
    
    print(f"\n🎯 Ready to call {phone_number}")
    print(f"📝 Message: {user_prompt}")
    
    confirm = input("\n✅ Proceed with AI test call? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    try:
        client = signalwire_client(
            project_id, 
            api_token, 
            signalwire_space_url=space_url
        )
        
        # Prepare call context
        call_context = {
            'user_prompt': user_prompt,
            'caller_context': 'Testing AI agent functionality'
        }
        
        # Create webhook URL with context
        context_params = urlencode({'call_context': json.dumps(call_context)})
        webhook_url = f"{host_app}/ai-agent?{context_params}"
        
        print(f"\n🔗 Full webhook URL: {webhook_url}")
        
        # Make the call
        call = client.calls.create(
            url=webhook_url,
            to=phone_number,
            from_=from_number,
            method='POST'
        )
        
        print(f"\n✅ AI Call initiated!")
        print(f"📋 Call SID: {call.sid}")
        print(f"📊 Status: {call.status}")
        print(f"\n🎉 The AI agent should be calling now!")
        print(f"📞 Answer the phone - you should hear the AI speaking!")
        print(f"\n💡 When you answer:")
        print(f"   1. You'll hear the AI greet you")
        print(f"   2. The AI will say the test message")
        print(f"   3. Please respond 'yes' if you can hear it")
        print(f"   4. Have a brief conversation!")
        
    except Exception as e:
        print(f"\n❌ Call failed: {str(e)}")

if __name__ == "__main__":
    test_ai_call() 