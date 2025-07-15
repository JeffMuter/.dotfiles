#!/bin/bash

# CallHiss Environment Setup Script
echo "🎵 CallHiss Environment Setup"
echo "============================="

# Set the SignalWire credentials
export SPACE_URL=saorsadev.signalwire.com
export PROJECT_ID=8cbde92d-5678-43ed-8c37-e5655182097
export API_TOKEN=PTdf9d22445677bb1f81962e7c14d907d6671d6eeff891f476
export FROM_NUMBER=+16144126309
export PORT=3000

# Get ngrok URL from the ngrok API
echo "🔍 Getting ngrok URL..."
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)

if [ "$NGROK_URL" != "null" ] && [ -n "$NGROK_URL" ]; then
    export HOST_APP=$NGROK_URL
    echo "✅ Found ngrok URL: $NGROK_URL"
    echo "🌐 HOST_APP set to: $HOST_APP"
else
    echo "❌ Could not get ngrok URL automatically"
    echo "📝 Please enter your ngrok URL manually:"
    echo "   (Look for the https://xxxx.ngrok.io URL in your ngrok terminal)"
    read -p "Enter ngrok URL: " MANUAL_URL
    export HOST_APP=$MANUAL_URL
    echo "🌐 HOST_APP set to: $HOST_APP"
fi

echo ""
echo "📚 Environment Variables Set:"
echo "   SPACE_URL=$SPACE_URL"
echo "   PROJECT_ID=$PROJECT_ID"
echo "   API_TOKEN=$API_TOKEN"
echo "   FROM_NUMBER=$FROM_NUMBER"
echo "   HOST_APP=$HOST_APP"
echo "   PORT=$PORT"
echo ""
echo "🚀 Ready to run CallHiss!"
echo "   Run: python call_hiss.py"
echo "" 