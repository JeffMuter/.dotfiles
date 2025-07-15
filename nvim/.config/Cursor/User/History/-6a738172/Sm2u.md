# pyDial Credential Test Suite

This test file verifies that your pyDial setup is correctly configured before making actual phone calls.

## Usage

```bash
# 1. Make sure you have sourced your config.env
source config.env

# 2. Run the credential tests
python test_credentials.py
```

## What it tests

### ✅ **Environment Variables**
- Checks that all required environment variables are set
- Validates that placeholder values have been replaced with real credentials

### 🌐 **SignalWire Configuration**
- Tests SignalWire API authentication
- Validates space URL format
- Checks phone number format
- Verifies that your FROM_NUMBER exists in your SignalWire account

### 🤖 **Anthropic AI Configuration**
- Tests Anthropic API authentication
- Validates API key format
- Makes a test API call to ensure the service is working

### 🔗 **Webhook Configuration**
- Validates HOST_APP URL format
- Checks for common configuration issues (localhost, placeholder values)

### 🌐 **Network Connectivity**
- Tests connectivity to SignalWire and Anthropic APIs
- Identifies network or firewall issues

## Expected Output

When everything is working correctly:
```
🎉 All tests passed! Your pyDial setup is ready to go.
   You can now run: python pydial.py
```

When there are issues:
```
❌ Some tests failed. Please fix the issues above before using pyDial.
   Check your config.env file and run: source config.env
```

## Common Issues

### Missing Environment Variables
- **Solution**: Copy `config.env.example` to `config.env` and fill in your credentials
- **Then run**: `source config.env`

### SignalWire Authentication Failed
- **Check**: Your SPACE_URL, PROJECT_ID, and API_TOKEN are correct
- **Verify**: You're using credentials from the correct SignalWire space

### Phone Number Not Found
- **Check**: Your FROM_NUMBER matches a number in your SignalWire account
- **Verify**: The number format includes the country code (e.g., +1234567890)

### Anthropic API Failed
- **Check**: Your ANTHROPIC_API_KEY is valid and not a placeholder
- **Verify**: You have sufficient API credits

### Webhook URL Issues
- **For local testing**: Use ngrok to create a public URL
- **For production**: Use a proper domain name
- **Never use**: localhost or 127.0.0.1 (SignalWire can't reach these)

## Running in CI/CD

This test file is designed for local use only. For GitHub Actions or other CI/CD systems, you'll need separate tests that don't require real API credentials. 