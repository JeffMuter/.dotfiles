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
    echo "3. Run the application: python call_hiss.py"
    echo ""
    echo "📚 Required Environment Variables:"
    echo "   export SPACE_URL=your_signalwire_space_url"
    echo "   export PROJECT_ID=your_signalwire_project_id"
    echo "   export API_TOKEN=your_signalwire_api_token"
    echo "   export FROM_NUMBER=your_signalwire_phone_number"
    echo "   export HOST_APP=http://your_public_url:3000  # For webhooks"
    echo "   export PORT=3000  # Optional, defaults to 3000"
    echo ""
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