#!/usr/bin/env python3
"""
Quick test for new API token
Replace the api_token below with your new token and run this script
"""

import requests
import base64

def test_new_token():
    print("🔑 Testing New API Token")
    print("=" * 30)
    
    # UPDATE THIS WITH YOUR NEW TOKEN
    space_url = "saorsadev.signalwire.com"
    project_id = "8cbde92d-5678-43ed-8c37-e56551820972"
    api_token = "PUT_YOUR_NEW_TOKEN_HERE"  # ← UPDATE THIS
    
    if api_token == "PUT_YOUR_NEW_TOKEN_HERE":
        print("❌ Please update the api_token in this script with your new token")
        return
    
    print(f"Testing with new token: {api_token[:10]}...")
    
    try:
        credentials = f"{project_id}:{api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        # Test the API
        api_url = f"https://{space_url}/api/laml/2010-04-01/Accounts/{project_id}.json"
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ NEW TOKEN WORKS!")
            data = response.json()
            print(f"Account SID: {data.get('sid')}")
            print(f"Account Status: {data.get('status')}")
            print("\n🎉 You can now update config.env and use CallHiss!")
        else:
            print(f"❌ Still getting error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_new_token() 