{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Python and development tools
    python311
    python311Packages.pip
    python311Packages.virtualenv
    python311Packages.setuptools
    python311Packages.wheel
    
    # Basic Python packages available in Nix
    python311Packages.flask
    python311Packages.requests
    python311Packages.urllib3
    
    # Development tools
    git
    curl
    jq
    ngrok  # For exposing local webhooks
    
    # Text editor (optional)
    nano
    vim
  ];

  shellHook = ''
    echo "🎵 CallHiss Development Environment"
    echo "=================================="
    echo ""
    echo "📦 Python version: $(python --version)"
    echo ""
    echo "🔧 Setup Instructions:"
    echo "1. Install Python dependencies: pip install -r requirements.txt"
    echo "2. Set up your environment variables (see config.env.example)"
    echo "3. Set up ngrok: ngrok config add-authtoken YOUR_TOKEN"
    echo "4. Start ngrok: ngrok http 3000"
    echo "5. Update HOST_APP with ngrok URL"
    echo "6. Run the application: python call_hiss.py"
    echo ""
    echo "📚 Required Environment Variables:"
    echo "   export SPACE_URL=saorsadev"
    echo "   export PROJECT_ID=8cbde92d-5678-43ed-8c37-e5655182097"
    echo "   export API_TOKEN=PTdf9d22445677bb1f81962e7c14d907d6671d6eeff891f476"
    echo "   export FROM_NUMBER=+16144126309"
    echo "   export HOST_APP=https://your-ngrok-url.ngrok.io  # Update with actual ngrok URL"
    echo "   export PORT=3000  # Optional, defaults to 3000"
    echo ""
    echo "🌐 ngrok available: $(which ngrok 2>/dev/null && echo "✅ Ready" || echo "❌ Not found")"
    echo "🚀 Ready to make AI-powered phone calls!"
    echo ""
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
      echo "🔨 Creating Python virtual environment..."
      python -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
      echo "📦 Installing Python dependencies..."
      pip install --upgrade pip
      pip install -r requirements.txt
      echo "✅ Dependencies installed!"
      echo ""
      echo "🌐 Flask version: $(python -c "import flask; print(flask.__version__)" 2>/dev/null || echo "Not installed")"
      echo "📞 SignalWire version: $(python -c "import signalwire; print(signalwire.__version__)" 2>/dev/null || echo "Not installed")"
    fi
  '';
  
  # Environment variables that should be set
  NIX_SHELL_PRESERVE_PROMPT = 1;
} 