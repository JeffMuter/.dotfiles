#!/usr/bin/env python3
"""
Credential and API Connectivity Test Suite for pyDial
Run this locally to verify your setup before making calls.

Usage: python test_credentials.py
"""

import os
import sys
import json
from datetime import datetime
from signalwire.rest import Client as signalwire_client
import anthropic
import requests
from urllib.parse import urlparse

class CredentialTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def log_test(self, test_name, passed, message, details=None):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.results.append({
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
        if passed:
            self.passed += 1
        else:
            self.failed += 1
            
        print(f"{status}: {test_name}")
        print(f"   {message}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_environment_variables(self):
        """Test that all required environment variables are set"""
        print("🔍 Testing Environment Variables...")
        
        required_vars = {
            'SPACE_URL': 'SignalWire Space URL',
            'PROJECT_ID': 'SignalWire Project ID', 
            'API_TOKEN': 'SignalWire API Token',
            'FROM_NUMBER': 'SignalWire Phone Number',
            'ANTHROPIC_API_KEY': 'Anthropic API Key'
        }
        
        missing_vars = []
        invalid_vars = []
        
        for var, description in required_vars.items():
            value = os.getenv(var)
            if not value:
                missing_vars.append(f"{var} ({description})")
            elif value in ['your_key_here', 'your-project-id-here', 'your-api-token-here', 'yourspace.signalwire.com']:
                invalid_vars.append(f"{var} (still has placeholder value)")
        
        if missing_vars:
            self.log_test(
                "Environment Variables - Missing",
                False,
                f"Missing {len(missing_vars)} required environment variables",
                f"Missing: {', '.join(missing_vars)}"
            )
        elif invalid_vars:
            self.log_test(
                "Environment Variables - Invalid",
                False,
                f"{len(invalid_vars)} variables have placeholder values",
                f"Update: {', '.join(invalid_vars)}"
            )
        else:
            self.log_test(
                "Environment Variables",
                True,
                "All required environment variables are set"
            )
    
    def test_space_url_format(self):
        """Test SignalWire space URL format"""
        print("🌐 Testing Space URL Format...")
        
        space_url = os.getenv('SPACE_URL')
        if not space_url:
            self.log_test(
                "Space URL Format",
                False,
                "SPACE_URL environment variable not set"
            )
            return
        
        # Check if it ends with .signalwire.com
        if not space_url.endswith('.signalwire.com'):
            # Try to fix it
            if '.' not in space_url:
                fixed_url = f"{space_url}.signalwire.com"
                self.log_test(
                    "Space URL Format",
                    True,
                    f"Space URL will be auto-corrected to: {fixed_url}",
                    f"Original: {space_url}"
                )
            else:
                self.log_test(
                    "Space URL Format",
                    False,
                    "Space URL should end with .signalwire.com",
                    f"Current: {space_url}"
                )
        else:
            self.log_test(
                "Space URL Format",
                True,
                f"Space URL format is correct: {space_url}"
            )
    
    def test_phone_number_format(self):
        """Test FROM_NUMBER format"""
        print("📞 Testing Phone Number Format...")
        
        from_number = os.getenv('FROM_NUMBER')
        if not from_number:
            self.log_test(
                "Phone Number Format",
                False,
                "FROM_NUMBER environment variable not set"
            )
            return
        
        # Basic format validation
        if not from_number.startswith('+'):
            self.log_test(
                "Phone Number Format",
                False,
                "Phone number should start with + (country code)",
                f"Current: {from_number}"
            )
        elif len(from_number) < 10:
            self.log_test(
                "Phone Number Format",
                False,
                "Phone number appears too short",
                f"Current: {from_number}"
            )
        else:
            self.log_test(
                "Phone Number Format",
                True,
                f"Phone number format looks correct: {from_number}"
            )
    
    def test_signalwire_authentication(self):
        """Test SignalWire API authentication"""
        print("🔐 Testing SignalWire Authentication...")
        
        space_url = os.getenv('SPACE_URL')
        project_id = os.getenv('PROJECT_ID')
        api_token = os.getenv('API_TOKEN')
        
        if not all([space_url, project_id, api_token]):
            self.log_test(
                "SignalWire Authentication",
                False,
                "Missing SignalWire credentials"
            )
            return
        
        # Fix space URL format if needed
        if not space_url.endswith('.signalwire.com'):
            space_url = f"{space_url}.signalwire.com"
        
        try:
            client = signalwire_client(
                project_id,
                api_token,
                signalwire_space_url=space_url
            )
            
            # Test with account fetch
            account = client.api.account.fetch()
            
            self.log_test(
                "SignalWire Authentication",
                True,
                f"Authentication successful! Account SID: {account.sid}",
                f"Account Name: {getattr(account, 'friendly_name', 'N/A')}"
            )
            
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                self.log_test(
                    "SignalWire Authentication",
                    False,
                    "Authentication failed - Invalid credentials",
                    f"Error: {error_msg}"
                )
            elif "404" in error_msg or "Not Found" in error_msg:
                self.log_test(
                    "SignalWire Authentication",
                    False,
                    "Authentication failed - Space URL or Project ID not found",
                    f"Error: {error_msg}"
                )
            else:
                self.log_test(
                    "SignalWire Authentication",
                    False,
                    f"Authentication failed - {error_msg}",
                    f"Space: {space_url}, Project: {project_id[:8]}..."
                )
    
    def test_signalwire_phone_numbers(self):
        """Test SignalWire phone number access"""
        print("📱 Testing SignalWire Phone Numbers...")
        
        space_url = os.getenv('SPACE_URL')
        project_id = os.getenv('PROJECT_ID')
        api_token = os.getenv('API_TOKEN')
        from_number = os.getenv('FROM_NUMBER')
        
        if not all([space_url, project_id, api_token]):
            self.log_test(
                "SignalWire Phone Numbers",
                False,
                "Missing SignalWire credentials"
            )
            return
        
        # Fix space URL format if needed
        if not space_url.endswith('.signalwire.com'):
            space_url = f"{space_url}.signalwire.com"
        
        try:
            client = signalwire_client(
                project_id,
                api_token,
                signalwire_space_url=space_url
            )
            
            # Get available phone numbers
            phone_numbers = client.incoming_phone_numbers.list(limit=20)
            
            if not phone_numbers:
                self.log_test(
                    "SignalWire Phone Numbers",
                    False,
                    "No phone numbers found in your SignalWire account",
                    "You need to purchase a phone number to make calls"
                )
                return
            
            # Check if FROM_NUMBER is in the list
            available_numbers = [pn.phone_number for pn in phone_numbers]
            
            if from_number and from_number in available_numbers:
                self.log_test(
                    "SignalWire Phone Numbers",
                    True,
                    f"FROM_NUMBER {from_number} is available in your account",
                    f"Total numbers available: {len(available_numbers)}"
                )
            elif from_number:
                self.log_test(
                    "SignalWire Phone Numbers",
                    False,
                    f"FROM_NUMBER {from_number} not found in your account",
                    f"Available: {', '.join(available_numbers[:3])}{'...' if len(available_numbers) > 3 else ''}"
                )
            else:
                self.log_test(
                    "SignalWire Phone Numbers",
                    True,
                    f"Found {len(available_numbers)} phone numbers in your account",
                    f"Available: {', '.join(available_numbers[:3])}{'...' if len(available_numbers) > 3 else ''}"
                )
                
        except Exception as e:
            self.log_test(
                "SignalWire Phone Numbers",
                False,
                f"Failed to retrieve phone numbers: {str(e)}"
            )
    
    def test_anthropic_authentication(self):
        """Test Anthropic API authentication"""
        print("🤖 Testing Anthropic AI Authentication...")
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key:
            self.log_test(
                "Anthropic Authentication",
                False,
                "ANTHROPIC_API_KEY environment variable not set"
            )
            return
        
        if api_key == 'your_anthropic_api_key_here':
            self.log_test(
                "Anthropic Authentication",
                False,
                "ANTHROPIC_API_KEY still has placeholder value"
            )
            return
        
        try:
            client = anthropic.Anthropic(api_key=api_key)
            
            # Test with a simple message
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[
                    {"role": "user", "content": "Say 'test successful'"}
                ]
            )
            
            response_text = message.content[0].text.strip()
            
            self.log_test(
                "Anthropic Authentication",
                True,
                "Anthropic API authentication successful",
                f"Test response: '{response_text}'"
            )
            
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "authentication" in error_msg.lower():
                self.log_test(
                    "Anthropic Authentication",
                    False,
                    "Anthropic API authentication failed - Invalid API key",
                    f"Error: {error_msg}"
                )
            elif "rate" in error_msg.lower() or "quota" in error_msg.lower():
                self.log_test(
                    "Anthropic Authentication",
                    False,
                    "Anthropic API rate limit or quota exceeded",
                    f"Error: {error_msg}"
                )
            else:
                self.log_test(
                    "Anthropic Authentication",
                    False,
                    f"Anthropic API test failed: {error_msg}"
                )
    
    def test_network_connectivity(self):
        """Test network connectivity to required services"""
        print("🌐 Testing Network Connectivity...")
        
        services = {
            'SignalWire API': 'https://api.signalwire.com',
            'Anthropic API': 'https://api.anthropic.com'
        }
        
        all_passed = True
        details = []
        
        for service_name, url in services.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code in [200, 401, 403]:  # 401/403 means we reached the service
                    details.append(f"{service_name}: ✅ Reachable")
                else:
                    details.append(f"{service_name}: ⚠️ Unexpected status {response.status_code}")
                    all_passed = False
            except requests.exceptions.Timeout:
                details.append(f"{service_name}: ❌ Timeout")
                all_passed = False
            except requests.exceptions.ConnectionError:
                details.append(f"{service_name}: ❌ Connection failed")
                all_passed = False
            except Exception as e:
                details.append(f"{service_name}: ❌ Error: {str(e)}")
                all_passed = False
        
        self.log_test(
            "Network Connectivity",
            all_passed,
            "All services reachable" if all_passed else "Some services unreachable",
            "; ".join(details)
        )
    
    def test_webhook_url_format(self):
        """Test webhook URL configuration"""
        print("🔗 Testing Webhook URL Configuration...")
        
        host_app = os.getenv('HOST_APP')
        port = os.getenv('PORT', '3000')
        
        if not host_app:
            self.log_test(
                "Webhook URL Configuration",
                False,
                "HOST_APP environment variable not set",
                "This is required for SignalWire to send webhooks back to your app"
            )
            return
        
        # Parse the URL
        try:
            parsed = urlparse(host_app)
            
            if not parsed.scheme:
                self.log_test(
                    "Webhook URL Configuration",
                    False,
                    "HOST_APP should include protocol (http:// or https://)",
                    f"Current: {host_app}"
                )
            elif parsed.scheme not in ['http', 'https']:
                self.log_test(
                    "Webhook URL Configuration",
                    False,
                    "HOST_APP should use http:// or https://",
                    f"Current: {host_app}"
                )
            elif 'localhost' in host_app or '127.0.0.1' in host_app:
                self.log_test(
                    "Webhook URL Configuration",
                    False,
                    "HOST_APP uses localhost - SignalWire cannot reach this",
                    "Use ngrok or a public URL for webhooks to work"
                )
            elif 'placeholder' in host_app.lower():
                self.log_test(
                    "Webhook URL Configuration",
                    False,
                    "HOST_APP still has placeholder value",
                    "Run setup_env.sh to configure ngrok or set a public URL"
                )
            else:
                self.log_test(
                    "Webhook URL Configuration",
                    True,
                    f"Webhook URL looks correct: {host_app}",
                    f"Port: {port}"
                )
                
        except Exception as e:
            self.log_test(
                "Webhook URL Configuration",
                False,
                f"Invalid HOST_APP URL format: {str(e)}",
                f"Current: {host_app}"
            )
    
    def run_all_tests(self):
        """Run all credential and connectivity tests"""
        print("🎵 pyDial Credential & API Test Suite")
        print("=" * 50)
        print()
        
        # Run all tests
        self.test_environment_variables()
        self.test_space_url_format()
        self.test_phone_number_format()
        self.test_webhook_url_format()
        self.test_network_connectivity()
        self.test_signalwire_authentication()
        self.test_signalwire_phone_numbers()
        self.test_anthropic_authentication()
        
        # Print summary
        print("=" * 50)
        print(f"📊 Test Summary: {self.passed} passed, {self.failed} failed")
        
        if self.failed == 0:
            print("🎉 All tests passed! Your pyDial setup is ready to go.")
            print("   You can now run: python pydial.py")
        else:
            print("❌ Some tests failed. Please fix the issues above before using pyDial.")
            print("   Check your config.env file and run: source config.env")
        
        print()
        return self.failed == 0

def main():
    """Main function to run credential tests"""
    # Check if config.env exists
    if not os.path.exists('config.env'):
        print("❌ config.env file not found!")
        print("   1. Copy config.env.example to config.env")
        print("   2. Fill in your credentials")
        print("   3. Run: source config.env")
        print("   4. Run this test again")
        sys.exit(1)
    
    # Remind user to source config.env
    required_vars = ['SPACE_URL', 'PROJECT_ID', 'API_TOKEN']
    if not any(os.getenv(var) for var in required_vars):
        print("⚠️  Environment variables not loaded!")
        print("   Run: source config.env")
        print("   Then run this test again")
        sys.exit(1)
    
    tester = CredentialTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 