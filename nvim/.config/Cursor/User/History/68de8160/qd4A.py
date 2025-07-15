#!/usr/bin/env python3
"""
SignalWire Credential Verification Tool
Run this before using CallHiss to verify your credentials are working
"""

import os
import sys
from signalwire.rest import Client as signalwire_client

def verify_credentials():
    print("🔐 SignalWire Credential Verification")
    print("=" * 45)
    
    # Check if environment variables are set
    space_url = os.getenv('SPACE_URL')
    project_id = os.getenv('PROJECT_ID')
    api_token = os.getenv('API_TOKEN')
    from_number = os.getenv('FROM_NUMBER')
    
    print("📋 Checking environment variables...")
    
    missing_vars = []
    if not space_url:
        missing_vars.append('SPACE_URL')
    if not project_id:
        missing_vars.append('PROJECT_ID')
    if not api_token:
        missing_vars.append('API_TOKEN')
    if not from_number:
        missing_vars.append('FROM_NUMBER')
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\n🔧 To fix this:")
        print("1. Edit config.env with your SignalWire credentials")
        print("2. Run: source config.env")
        print("3. Run this script again")
        return False
    
    print("✅ All environment variables are set")
    
    # Fix space URL format
    if not space_url.endswith('.signalwire.com'):
        space_url = f"{space_url}.signalwire.com"
    
    print(f"\n📡 Testing connection to {space_url}...")
    print(f"   Project ID: {project_id}")
    print(f"   API Token: {api_token[:8]}...")
    print(f"   From Number: {from_number}")
    
    try:
        # Test SignalWire connection
        client = signalwire_client(
            project_id, 
            api_token, 
            signalwire_space_url=space_url
        )
        
        # Fetch account info
        account = client.api.account.fetch()
        print(f"\n✅ Authentication successful!")
        print(f"   Account SID: {account.sid}")
        print(f"   Account Status: {account.status}")
        print(f"   Account Type: {account.type}")
        
        # Check phone numbers
        print(f"\n📞 Checking phone numbers...")
        phone_numbers = client.incoming_phone_numbers.list(limit=10)
        
        if not phone_numbers:
            print("⚠️  No phone numbers found in this account")
            print("   You need at least one phone number to make calls")
            return False
        
        print(f"   Found {len(phone_numbers)} phone number(s):")
        from_number_found = False
        
        for number in phone_numbers:
            status = "✅" if number.phone_number == from_number else "  "
            print(f"   {status} {number.phone_number} - {number.friendly_name}")
            if number.phone_number == from_number:
                from_number_found = True
        
        if not from_number_found:
            print(f"\n⚠️  FROM_NUMBER {from_number} not found in your account")
            print("   Please update FROM_NUMBER in config.env to one of the numbers above")
            return False
        
        print(f"\n🎉 All credentials verified successfully!")
        print("   You're ready to use CallHiss!")
        return True
        
    except Exception as e:
        print(f"\n❌ Authentication failed!")
        print(f"   Error: {str(e)}")
        
        if "401" in str(e) or "Unauthorized" in str(e):
            print(f"\n🔍 This is a 401 Unauthorized error. Common causes:")
            print(f"   1. Incorrect API Token")
            print(f"   2. Incorrect Project ID") 
            print(f"   3. Credentials from wrong SignalWire Space")
            print(f"   4. Expired or revoked API Token")
            print(f"\n🔧 To fix:")
            print(f"   1. Go to https://signalwire.com/signin")
            print(f"   2. Select your space: {space_url.replace('.signalwire.com', '')}")
            print(f"   3. Go to API section")
            print(f"   4. Copy the correct Project ID and API Token")
            print(f"   5. Update config.env")
            print(f"   6. Run: source config.env")
        
        return False

if __name__ == "__main__":
    print("🎵 CallHiss - Credential Verification")
    print()
    
    if verify_credentials():
        print("\n🚀 Ready to make AI-powered phone calls!")
        print("   Run: python call_hiss.py")
    else:
        print("\n❌ Please fix the issues above before using CallHiss")
        sys.exit(1) 