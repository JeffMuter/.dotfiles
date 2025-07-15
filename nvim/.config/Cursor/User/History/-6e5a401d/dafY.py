#!/usr/bin/env python3
"""
Test script to debug SignalWire authentication issues
"""

import os
from signalwire.rest import Client as signalwire_client

def test_signalwire_auth():
    # Load environment variables
    space_url = os.getenv('SPACE_URL')
    project_id = os.getenv('PROJECT_ID')
    api_token = os.getenv('API_TOKEN')
    
    print("🔍 Testing SignalWire Authentication")
    print("=" * 40)
    print(f"Space URL: {space_url}")
    print(f"Project ID: {project_id}")
    print(f"API Token: {api_token[:10]}..." if api_token else "None")
    print()
    
    if not all([space_url, project_id, api_token]):
        print("❌ Missing required environment variables!")
        return False
    
    # Test 1: Check space URL format
    if not space_url.endswith('.signalwire.com'):
        print(f"⚠️  Space URL might be incomplete: {space_url}")
        print(f"   Trying with .signalwire.com suffix...")
        space_url = f"{space_url}.signalwire.com"
        print(f"   Updated Space URL: {space_url}")
    
    try:
        # Initialize client
        print("🔗 Initializing SignalWire client...")
        client = signalwire_client(
            project_id, 
            api_token, 
            signalwire_space_url=space_url
        )
        
        # Test 2: Fetch account info
        print("📋 Fetching account information...")
        account = client.api.account.fetch()
        print(f"✅ Authentication successful!")
        print(f"   Account SID: {account.sid}")
        print(f"   Account Status: {account.status}")
        
        # Test 3: List phone numbers
        print("📞 Fetching phone numbers...")
        phone_numbers = client.incoming_phone_numbers.list(limit=5)
        print(f"   Found {len(phone_numbers)} phone numbers")
        for number in phone_numbers:
            print(f"   - {number.phone_number} ({number.friendly_name})")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed!")
        print(f"   Error: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        
        # Additional debugging
        if "401" in str(e):
            print("\n🔍 401 Unauthorized Error Detected:")
            print("   Possible causes:")
            print("   1. Incorrect API Token")
            print("   2. Incorrect Project ID")
            print("   3. Incorrect Space URL")
            print("   4. Token expired or revoked")
            print("   5. Account suspended")
        
        return False

if __name__ == "__main__":
    test_signalwire_auth() 