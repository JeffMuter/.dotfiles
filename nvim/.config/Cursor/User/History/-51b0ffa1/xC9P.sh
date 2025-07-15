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

# Run the application using venv python directly
echo "🚀 Starting pyDial with virtual environment..."
venv/bin/python pydial.py "$@" 