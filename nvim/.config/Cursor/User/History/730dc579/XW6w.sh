#!/bin/bash

# CallHiss Environment Setup Script
echo "🎵 CallHiss Environment Setup"
echo "============================="

# Load configuration from config.env
if [ -f "config.env" ]; then
    echo "🔧 Loading configuration from config.env..."
    source config.env
    echo "✅ Configuration loaded!"
else
    echo "❌ config.env not found!"
    echo "   Please create config.env with your credentials first"
    exit 1
fi

# Get ngrok URL from the ngrok API
echo "🔍 Getting ngrok URL..."
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)

if [ "$NGROK_URL" != "null" ] && [ -n "$NGROK_URL" ]; then
    echo "✅ Found ngrok URL: $NGROK_URL"
    
    # Update HOST_APP in config.env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|^export HOST_APP=.*|export HOST_APP=$NGROK_URL|" config.env
    else
        # Linux
        sed -i "s|^export HOST_APP=.*|export HOST_APP=$NGROK_URL|" config.env
    fi
    
    export HOST_APP=$NGROK_URL
    echo "🌐 HOST_APP updated in config.env: $HOST_APP"
else
    echo "❌ Could not get ngrok URL automatically"
    echo "📝 Please enter your ngrok URL manually:"
    echo "   (Look for the https://xxxx.ngrok.io URL in your ngrok terminal)"
    read -p "Enter ngrok URL: " MANUAL_URL
    
    if [ -n "$MANUAL_URL" ]; then
        # Update HOST_APP in config.env
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|^export HOST_APP=.*|export HOST_APP=$MANUAL_URL|" config.env
        else
            # Linux
            sed -i "s|^export HOST_APP=.*|export HOST_APP=$MANUAL_URL|" config.env
        fi
        
        export HOST_APP=$MANUAL_URL
        echo "🌐 HOST_APP updated in config.env: $HOST_APP"
    fi
fi

echo ""
echo "📚 Current Configuration:"
echo "   SPACE_URL=$SPACE_URL"
echo "   PROJECT_ID=$PROJECT_ID"
echo "   FROM_NUMBER=$FROM_NUMBER"
echo "   HOST_APP=$HOST_APP"
echo "   PORT=$PORT"
echo "   AI_VOICE=$AI_VOICE"
echo ""
echo "🚀 Ready to run CallHiss!"
echo "   Run: python call_hiss.py"
echo "" 