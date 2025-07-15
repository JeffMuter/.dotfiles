#!/bin/bash

# pyDial Runner Script
# This ensures the virtual environment Python is used and config is loaded

# Check if we're in the right directory
if [ ! -f "pydial.py" ]; then
    echo "❌ Error: pydial.py not found. Please run this script from the pyDial directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run 'nix-shell' first to set up the environment."
    exit 1
fi

# Load configuration from config.env
if [ -f "config.env" ]; then
    echo "🔧 Loading configuration from config.env..."
    source config.env
    echo "✅ Configuration loaded!"
else
    echo "❌ Error: config.env not found. Please create it from config.env.example"
    exit 1
fi

# Check if dependencies are installed using venv python directly
if ! venv/bin/python -c "import flask, signalwire, anthropic" >/dev/null 2>&1; then
    echo "❌ Error: Dependencies not installed. Please run 'nix-shell' first to install dependencies."
    exit 1
fi

# Verify essential environment variables are set
if [ -z "$HOST_APP" ] || [ -z "$SPACE_URL" ] || [ -z "$PROJECT_ID" ] || [ -z "$API_TOKEN" ]; then
    echo "❌ Error: Essential environment variables not set in config.env"
    echo "   Please check: HOST_APP, SPACE_URL, PROJECT_ID, API_TOKEN"
    exit 1
fi

echo "🌐 Using webhook URL: $HOST_APP"

# Check if ngrok is running (only if HOST_APP contains ngrok)
if [[ "$HOST_APP" == *"ngrok"* ]]; then
    echo "🔍 Checking if ngrok is running..."
    
    # Check if ngrok URL returns a proper response (not 404)
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$HOST_APP" 2>/dev/null || echo "000")
    
    if [ "$HTTP_CODE" = "000" ]; then
        echo "❌ Error: Cannot reach ngrok URL!"
        echo ""
        echo "🔧 To fix this:"
        echo "   1. Open a NEW terminal window"
        echo "   2. Navigate to this directory: cd $(pwd)"
        echo "   3. Run: ngrok http 3000"
        echo "   4. Copy the https:// URL from ngrok"
        echo "   5. Update HOST_APP in config.env with that URL"
        echo "   6. Come back to this terminal and run ./run.sh again"
        echo ""
        echo "💡 Tip: Keep ngrok running in that separate terminal while using pyDial"
        exit 1
    elif [ "$HTTP_CODE" = "404" ]; then
        echo "⚠️  ngrok is running but Flask server is not accessible"
        echo "   This is normal - the Flask server will start when you run pyDial"
        echo "   ngrok tunnel: ✅ Ready"
    else
        echo "✅ ngrok is running and accessible!"
    fi
fi

# Run the application using venv python directly
echo "🚀 Starting pyDial with virtual environment..."
venv/bin/python pydial.py "$@" 