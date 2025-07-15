#!/usr/bin/env python3
"""
SignalWire 401 Error Fix Script
This script helps identify and fix authentication issues
"""

import os
import requests
import base64
from signalwire.rest import Client as signalwire_client

def fix_401_issue():
    print("🔧 SignalWire 401 Error Fix")
    print("=" * 40)
    
    space_url = os.getenv('SPACE_URL')
    project_id = os.getenv('PROJECT_ID')
    api_token = os.getenv('API_TOKEN')
    
    if not space_url.endswith('.signalwire.com'):
        space_url = f"{space_url}.signalwire.com"
    
    print(f"Current credentials:")
    print(f"  Space: {space_url}")
    print(f"  Project: {project_id}")
    print(f"  Token: {api_token[:10]}...")
    print()
    
    # Test the correct SignalWire API endpoint
    print("🧪 Testing Compatibility API endpoint...")
    
    try:
        # Use the correct Twilio-compatible API endpoint
        credentials = f"{project_id}:{api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        # Correct API endpoint for SignalWire
        api_url = f"https://{space_url}/api/laml/2010-04-01/Accounts/{project_id}.json"
        print(f"Testing: {api_url}")
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            data = response.json()
            print(f"Account SID: {data.get('sid')}")
            print(f"Account Status: {data.get('status')}")
            return True
        elif response.status_code == 401:
            print("❌ 401 Unauthorized - Invalid credentials")
            print("Response:", response.text)
        else:
            print(f"❌ Error {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
    
    print()
    print("🔍 Possible Issues and Solutions:")
    print("-" * 40)
    
    print("1. INCORRECT CREDENTIALS")
    print("   → Log into SignalWire Dashboard")
    print("   → Go to your Space settings")
    print("   → Copy the correct Project ID and API Token")
    print()
    
    print("2. EXPIRED OR REVOKED TOKEN")
    print("   → Generate a new API token in the dashboard")
    print("   → Update your config.env file")
    print()
    
    print("3. ACCOUNT SUSPENDED")
    print("   → Check your account status in the dashboard")
    print("   → Contact SignalWire support if needed")
    print()
    
    print("4. WRONG SPACE")
    print("   → Verify you're using the correct space URL")
    print("   → Check if the project exists in this space")
    print()
    
    print("🔧 Quick Fix Steps:")
    print("-" * 40)
    print("1. Go to: https://signalwire.com/signin")
    print("2. Select your space (saorsadev)")
    print("3. Go to API section")
    print("4. Copy the Project ID and API Token")
    print("5. Update config.env with correct values")
    print("6. Run: source config.env && python call_hiss.py")
    
    return False

def test_fixed_credentials():
    """Test if the credentials work after fixing"""
    print("\n🧪 Testing Fixed Credentials...")
    
    try:
        space_url = os.getenv('SPACE_URL')
        project_id = os.getenv('PROJECT_ID')
        api_token = os.getenv('API_TOKEN')
        
        if not space_url.endswith('.signalwire.com'):
            space_url = f"{space_url}.signalwire.com"
        
        client = signalwire_client(
            project_id, 
            api_token, 
            signalwire_space_url=space_url
        )
        
        account = client.api.account.fetch()
        print("✅ Credentials are working!")
        print(f"Account SID: {account.sid}")
        print(f"Account Status: {account.status}")
        
        # Test phone numbers
        numbers = client.incoming_phone_numbers.list(limit=3)
        print(f"Phone numbers available: {len(numbers)}")
        for num in numbers:
            print(f"  - {num.phone_number}")
        
        return True
        
    except Exception as e:
        print(f"❌ Still not working: {str(e)}")
        return False

if __name__ == "__main__":
    if not fix_401_issue():
        print("\n" + "="*50)
        print("❌ AUTHENTICATION STILL FAILING")
        print("="*50)
        print("Please follow the steps above to fix your credentials.")
        print("Then run this script again to test.")
    else:
        test_fixed_credentials() 