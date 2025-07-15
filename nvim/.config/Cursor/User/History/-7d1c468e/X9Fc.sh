#!/bin/bash

# pyDial ngrok Setup Script
# This script starts ngrok and updates your config.env automatically

echo "🌐 pyDial ngrok Setup"
echo "===================="

# Check if ngrok is available
if ! command -v ngrok >/dev/null 2>&1; then
    echo "❌ Error: ngrok not found!"
    echo "   Please run 'nix-shell' first to set up the environment"
    exit 1
fi

# Check if config.env exists
if [ ! -f "config.env" ]; then
    echo "❌ Error: config.env not found!"
    echo "   Please create it from config.env.example first"
    exit 1
fi

# Kill any existing ngrok processes
echo "🔧 Stopping any existing ngrok processes..."
pkill -f "ngrok http" 2>/dev/null || true

# Start ngrok in the background
echo "🚀 Starting ngrok tunnel on port 3000..."
ngrok http 3000 --log=stdout > ngrok.log 2>&1 &
NGROK_PID=$!

# Wait a moment for ngrok to start
sleep 3

# Get the ngrok URL
echo "🔍 Getting ngrok URL..."
NGROK_URL=""
for i in {1..10}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o 'https://[^"]*\.ngrok-free\.app' | head -1)
    if [ -n "$NGROK_URL" ]; then
        break
    fi
    echo "   Waiting for ngrok to start... ($i/10)"
    sleep 1
done

if [ -z "$NGROK_URL" ]; then
    echo "❌ Error: Could not get ngrok URL!"
    echo "   Check ngrok.log for details"
    kill $NGROK_PID 2>/dev/null || true
    exit 1
fi

echo "✅ ngrok tunnel created: $NGROK_URL"

# Update config.env with the new URL
echo "🔧 Updating config.env with new ngrok URL..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|^export HOST_APP=.*|export HOST_APP=$NGROK_URL|" config.env
else
    # Linux
    sed -i "s|^export HOST_APP=.*|export HOST_APP=$NGROK_URL|" config.env
fi

echo "✅ config.env updated!"
echo ""
echo "🎉 Setup complete!"
echo "   ngrok URL: $NGROK_URL"
echo "   Process ID: $NGROK_PID"
echo ""
echo "📝 Next steps:"
echo "   1. Keep this terminal open (ngrok is running here)"
echo "   2. Open a NEW terminal"
echo "   3. Navigate to this directory"
echo "   4. Run: ./run.sh"
echo ""
echo "🛑 To stop ngrok later: kill $NGROK_PID"

# Keep the script running so ngrok stays active
echo "🔄 ngrok is running... Press Ctrl+C to stop"
wait $NGROK_PID 