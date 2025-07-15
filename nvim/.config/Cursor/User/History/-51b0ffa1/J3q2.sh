#!/bin/bash

# pyDial Runner Script
# This ensures the virtual environment Python is used

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

# Check if dependencies are installed using venv python directly
if ! venv/bin/python -c "import flask, signalwire, anthropic" >/dev/null 2>&1; then
    echo "❌ Error: Dependencies not installed. Please run 'nix-shell' first to install dependencies."
    exit 1
fi

# Run the application using venv python directly
echo "🚀 Starting pyDial with virtual environment..."
venv/bin/python pydial.py "$@" 