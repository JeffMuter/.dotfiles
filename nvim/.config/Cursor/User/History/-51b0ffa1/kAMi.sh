#!/bin/bash

# pyDial Runner Script
# This ensures the virtual environment is properly activated

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

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask, signalwire, anthropic" >/dev/null 2>&1; then
    echo "❌ Error: Dependencies not installed. Please run 'nix-shell' first to install dependencies."
    exit 1
fi

# Run the application
echo "🚀 Starting pyDial..."
python pydial.py "$@" 