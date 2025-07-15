#!/usr/bin/env python3
"""
Simple CallHiss Test - No webhooks required
This version makes AI calls without needing ngrok setup
"""

import os
from signalwire.rest import Client as signalwire_client

def make_simple_ai_call():
    print("🎵 Simple CallHiss Test")
    print("=" * 30)
    
    # Load credentials
    space_url = os.getenv('SPACE_URL')
    project_id = os.getenv('PROJECT_ID') 
    api_token = os.getenv('API_TOKEN')
    from_number = os.getenv('FROM_NUMBER')
    
    if not all([space_url, project_id, api_token, from_number]):
        print("❌ Missing environment variables. Run: source config.env")
        return
    
    if not space_url.endswith('.signalwire.com'):
        space_url = f"{space_url}.signalwire.com"
    
    # Get user input
    print("\n💭 What should the AI say?")
    user_prompt = input("> ").strip()
    
    if not user_prompt:
        print("❌ Please enter a message")
        return
    
    print("\n📞 Phone number to call:")
    phone_number = input("> ").strip()
    
    if not phone_number:
        print("❌ Please enter a phone number")
        return
    
    print(f"\n🎯 Ready to call {phone_number}")
    print(f"📝 Message: {user_prompt}")
    
    confirm = input("\n✅ Proceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    try:
        client = signalwire_client(
            project_id, 
            api_token, 
            signalwire_space_url=space_url
        )
        
        # Create TwiML for the AI call
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <AI voice="en-US-Neural2-D">
            <Prompt confidence="0.6" frequency_penalty="0.3">
                You are an AI assistant making a phone call. 
                
                Your task: {user_prompt}
                
                Instructions:
                1. Greet the person politely
                2. Deliver the message naturally
                3. Handle any questions or responses
                4. Keep it brief and focused
                5. End the call politely
                
                Be natural, friendly, and complete your task efficiently.
            </Prompt>
        </AI>
    </Connect>
</Response>"""
        
        # Make the call with inline TwiML
        call = client.calls.create(
            twiml=twiml,
            to=phone_number,
            from_=from_number
        )
        
        print(f"\n✅ Call initiated!")
        print(f"📋 Call SID: {call.sid}")
        print(f"📊 Status: {call.status}")
        print(f"\n🎉 The AI should be calling now!")
        print(f"📞 Answer the phone and talk to the AI!")
        
    except Exception as e:
        print(f"\n❌ Call failed: {str(e)}")
        
        if "trial" in str(e).lower():
            print("\n🔍 Trial account limitation:")
            print("   Make sure you're calling a verified number")
            print("   Your verified number: +16145572867")

if __name__ == "__main__":
    make_simple_ai_call() 