#!/usr/bin/env python3
"""
Comprehensive 401 Error Debugging Script for SignalWire
"""

import os
import requests
import base64
from signalwire.rest import Client as signalwire_client

def debug_signalwire_401():
    print("🔍 SignalWire 401 Error Debugging")
    print("=" * 50)
    
    # Load environment variables
    space_url = os.getenv('SPACE_URL')
    project_id = os.getenv('PROJECT_ID')
    api_token = os.getenv('API_TOKEN')
    
    print(f"📋 Current Configuration:")
    print(f"   Space URL: {space_url}")
    print(f"   Project ID: {project_id}")
    print(f"   API Token: {api_token[:10]}..." if api_token else "None")
    print()
    
    if not all([space_url, project_id, api_token]):
        print("❌ Missing required environment variables!")
        return False
    
    # Fix space URL format if needed
    if not space_url.endswith('.signalwire.com'):
        space_url = f"{space_url}.signalwire.com"
        print(f"🔧 Fixed Space URL: {space_url}")
    
    # Test 1: Direct HTTP API call
    print("🌐 Test 1: Direct HTTP API Authentication")
    print("-" * 40)
    
    try:
        # Create basic auth header
        credentials = f"{project_id}:{api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        # Test URL
        test_url = f"https://{space_url}/api/relay/rest/accounts/{project_id}.json"
        print(f"   Testing URL: {test_url}")
        
        response = requests.get(test_url, headers=headers, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("   ✅ Direct HTTP authentication successful!")
            data = response.json()
            print(f"   Account SID: {data.get('sid', 'N/A')}")
        else:
            print(f"   ❌ Direct HTTP authentication failed!")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ HTTP request failed: {str(e)}")
    
    print()
    
    # Test 2: SignalWire SDK Authentication
    print("🔧 Test 2: SignalWire SDK Authentication")
    print("-" * 40)
    
    try:
        client = signalwire_client(
            project_id, 
            api_token, 
            signalwire_space_url=space_url
        )
        
        # Try to fetch account
        account = client.api.account.fetch()
        print("   ✅ SDK authentication successful!")
        print(f"   Account SID: {account.sid}")
        print(f"   Account Status: {account.status}")
        
    except Exception as e:
        print(f"   ❌ SDK authentication failed!")
        print(f"   Error: {str(e)}")
        print(f"   Error Type: {type(e).__name__}")
    
    print()
    
    # Test 3: Alternative Space URL formats
    print("🔄 Test 3: Alternative Space URL Formats")
    print("-" * 40)
    
    alternative_urls = [
        f"{space_url}",
        f"https://{space_url}",
        f"{space_url.replace('.signalwire.com', '')}.signalwire.com",
        f"saorsadev.signalwire.com"  # Direct format
    ]
    
    for alt_url in alternative_urls:
        try:
            print(f"   Testing: {alt_url}")
            client = signalwire_client(
                project_id, 
                api_token, 
                signalwire_space_url=alt_url
            )
            account = client.api.account.fetch()
            print(f"   ✅ Success with: {alt_url}")
            break
        except Exception as e:
            print(f"   ❌ Failed with: {alt_url} - {str(e)[:50]}...")
    
    print()
    
    # Test 4: Credential validation
    print("🔐 Test 4: Credential Format Validation")
    print("-" * 40)
    
    # Check Project ID format
    if len(project_id) == 36 and project_id.count('-') == 4:
        print("   ✅ Project ID format looks correct (UUID)")
    else:
        print(f"   ⚠️  Project ID format unusual: {len(project_id)} chars, {project_id.count('-')} dashes")
    
    # Check API Token format
    if len(api_token) >= 32:
        print("   ✅ API Token length looks reasonable")
    else:
        print(f"   ⚠️  API Token seems short: {len(api_token)} characters")
    
    # Check for common issues
    if ' ' in project_id or ' ' in api_token:
        print("   ⚠️  Credentials contain spaces - this could cause issues")
    
    if project_id.startswith('AC') or api_token.startswith('SK'):
        print("   ⚠️  Credentials look like Twilio format - make sure you're using SignalWire credentials")
    
    print()
    
    # Test 5: Network connectivity
    print("🌍 Test 5: Network Connectivity")
    print("-" * 40)
    
    try:
        response = requests.get(f"https://{space_url}", timeout=5)
        print(f"   ✅ Can reach {space_url} (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Cannot reach {space_url}: {str(e)}")
    
    print()
    
    # Recommendations
    print("💡 Troubleshooting Recommendations:")
    print("-" * 40)
    print("1. Verify credentials in SignalWire Dashboard:")
    print("   - Go to your SignalWire Space")
    print("   - Check API section for correct Project ID and Token")
    print("2. Ensure you're using SignalWire credentials (not Twilio)")
    print("3. Check if your account is active and not suspended")
    print("4. Try regenerating your API token in the dashboard")
    print("5. Verify your space URL is correct")
    print()
    print("🔗 SignalWire Dashboard: https://signalwire.com/signin")

if __name__ == "__main__":
    debug_signalwire_401() 