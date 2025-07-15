#!/usr/bin/env python3
"""
Test the exact credentials provided by the user
"""

import requests
import base64
from signalwire.rest import Client as signalwire_client

def test_credentials():
    print("🧪 Testing Exact Credentials from Dashboard")
    print("=" * 50)
    
    # Exact credentials from user
    space_url = "saorsadev.signalwire.com"
    project_id = "8cbde92d-5678-43ed-8c37-e56551820972"
    api_token = "PTdf9d22445677bb1f81962e7c14d907d6671d6eeff891f476"
    
    print(f"Space: {space_url}")
    print(f"Project: {project_id}")
    print(f"Token: {api_token}")
    print()
    
    # Test 1: Direct HTTP with correct endpoint
    print("🌐 Test 1: Direct HTTP API Call")
    print("-" * 30)
    
    try:
        credentials = f"{project_id}:{api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        # Test the correct SignalWire API endpoint
        api_url = f"https://{space_url}/api/laml/2010-04-01/Accounts/{project_id}.json"
        print(f"URL: {api_url}")
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ HTTP API works!")
            return True
        else:
            print("❌ HTTP API failed")
            
    except Exception as e:
        print(f"❌ HTTP Error: {str(e)}")
    
    print()
    
    # Test 2: SignalWire SDK
    print("🔧 Test 2: SignalWire SDK")
    print("-" * 30)
    
    try:
        client = signalwire_client(
            project_id, 
            api_token, 
            signalwire_space_url=space_url
        )
        
        account = client.api.account.fetch()
        print("✅ SDK works!")
        print(f"Account: {account.sid}")
        return True
        
    except Exception as e:
        print(f"❌ SDK Error: {str(e)}")
    
    print()
    
    # Test 3: Check if account exists at all
    print("🔍 Test 3: Account Existence Check")
    print("-" * 30)
    
    try:
        # Try to list accounts (this might work even if specific account fetch fails)
        list_url = f"https://{space_url}/api/laml/2010-04-01/Accounts.json"
        response = requests.get(list_url, headers=headers, timeout=10)
        
        print(f"List Accounts Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Can list accounts - credentials are valid!")
            data = response.json()
            print(f"Found {len(data.get('accounts', []))} accounts")
        else:
            print(f"❌ Cannot list accounts: {response.text}")
            
    except Exception as e:
        print(f"❌ List Error: {str(e)}")
    
    print()
    
    # Test 4: Check space accessibility
    print("🌐 Test 4: Space Accessibility")
    print("-" * 30)
    
    try:
        space_response = requests.get(f"https://{space_url}", timeout=5)
        print(f"Space URL Status: {space_response.status_code}")
        
        if space_response.status_code == 200:
            print("✅ Space is accessible")
        else:
            print("❌ Space not accessible")
            
    except Exception as e:
        print(f"❌ Space Error: {str(e)}")
    
    print()
    print("🔍 Diagnosis:")
    print("-" * 30)
    print("If all tests fail with 401, possible causes:")
    print("1. Account is suspended or inactive")
    print("2. API token was revoked after you copied it")
    print("3. Project doesn't exist in this space")
    print("4. There's a billing issue with your account")
    print("5. The credentials were copied incorrectly")
    print()
    print("💡 Next Steps:")
    print("1. Log into SignalWire dashboard and verify account status")
    print("2. Check if there are any billing issues")
    print("3. Try generating a completely new API token")
    print("4. Contact SignalWire support if the issue persists")
    
    return False

if __name__ == "__main__":
    test_credentials() 