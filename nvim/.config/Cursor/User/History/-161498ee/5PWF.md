# 🔧 pyDial Troubleshooting Guide

## 🔇 No Voice on Phone Call

**Symptoms:** The call connects but there's no voice/audio on the other end.

**Cause:** The webhook URL is not accessible to SignalWire, so the AI agent can't respond.

**Solution:**

1. **Check if ngrok is running:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" $HOST_APP
   ```
   - If you get `000`: ngrok is not running
   - If you get `404`: ngrok is running but Flask server isn't
   - If you get `200`: Everything is working

2. **Proper startup sequence:**
   ```bash
   # Terminal 1: Start ngrok
   ./start_ngrok.sh
   
   # Terminal 2: Start pyDial (in a NEW terminal)
   ./run.sh
   ```

3. **Verify the setup:**
   ```bash
   # Check that HOST_APP is set to ngrok URL
   echo $HOST_APP
   
   # Should show something like: https://abc123.ngrok-free.app
   ```

## 🔐 Authentication Errors

**Symptoms:** "401 Unauthorized" or "Authentication failed"

**Solutions:**

1. **Verify credentials:**
   ```bash
   python test_credentials.py
   ```

2. **Check environment variables:**
   ```bash
   echo "Space: $SPACE_URL"
   echo "Project: $PROJECT_ID" 
   echo "Token: ${API_TOKEN:0:10}..."  # Shows first 10 chars
   ```

3. **Re-source config:**
   ```bash
   source config.env
   ```

## 🌐 Network/Connection Issues

**Symptoms:** "Connection failed" or timeouts

**Solutions:**

1. **Test network connectivity:**
   ```bash
   curl -s https://api.signalwire.com
   curl -s https://api.anthropic.com
   ```

2. **Check firewall/proxy settings**

3. **Verify ngrok authentication:**
   ```bash
   ngrok config check
   ```

## 📞 Call Fails to Initiate

**Symptoms:** Call never starts or immediate failure

**Common causes:**

1. **FROM_NUMBER not in your account:**
   - Check SignalWire dashboard for your phone numbers
   - Ensure FROM_NUMBER matches exactly (including +1)

2. **Trial account limitations:**
   - Can only call verified numbers
   - Add billing to remove restrictions

3. **Invalid phone number format:**
   - Must include country code: +1234567890
   - No spaces, dashes, or parentheses

## 🤖 AI Responses Not Working

**Symptoms:** Call connects but AI gives error messages

**Solutions:**

1. **Check Anthropic API key:**
   ```bash
   echo "API Key: ${ANTHROPIC_API_KEY:0:15}..."
   ```

2. **Verify API credits:**
   - Check https://console.anthropic.com/
   - Ensure you have sufficient credits

3. **Test AI directly:**
   ```bash
   python -c "import anthropic; print('AI client works!')"
   ```

## 🔄 General Debugging

**Enable debug mode:**
```bash
# Add to config.env
export DEBUG=true

# Run with verbose output
./run.sh
```

**Check logs:**
```bash
# View ngrok logs
cat ngrok.log

# View Flask server output in terminal
```

**Reset everything:**
```bash
# Kill all processes
pkill -f ngrok
pkill -f python

# Restart fresh
./start_ngrok.sh  # Terminal 1
./run.sh          # Terminal 2
```

## 📋 Quick Checklist

Before making calls, verify:

- [ ] `config.env` exists and has real credentials
- [ ] `source config.env` has been run
- [ ] ngrok is running: `./start_ngrok.sh`
- [ ] Flask server is running: `./run.sh`
- [ ] HOST_APP points to ngrok URL
- [ ] FROM_NUMBER is in your SignalWire account
- [ ] Target number is verified (if trial account)
- [ ] Anthropic API key is valid and has credits

## 🆘 Still Having Issues?

1. **Run the credential test:**
   ```bash
   python test_credentials.py
   ```

2. **Check the complete setup:**
   ```bash
   ./run.sh --version  # Should show all green checkmarks
   ```

3. **Verify webhook accessibility:**
   ```bash
   curl -X POST $HOST_APP/ai-agent
   # Should return XML response, not 404
   ``` 