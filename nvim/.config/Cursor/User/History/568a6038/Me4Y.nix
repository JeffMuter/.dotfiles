{ pkgs ? import <nixpkgs> { config.allowUnfree = true; } }:

let
  # Create a Python environment with all required packages
  pythonEnv = pkgs.python311.withPackages (ps: with ps; [
    flask
    requests
    urllib3
    pip
    setuptools
    wheel
    # Note: signalwire and anthropic may not be available in nixpkgs
    # We'll handle these with pip in a proper virtual environment
  ]);
in

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Python environment with basic packages
    pythonEnv
    
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
    echo "🐍 pyDial Development Environment"
    echo "================================"
    echo ""
    echo "📦 Python version: $(python --version)"
    echo "🔧 Git version: $(git --version)"
    echo ""
    
    # Check Git status
    if [ -d ".git" ]; then
      echo "📋 Git Status:"
      echo "   Repository: $(git remote get-url origin 2>/dev/null || echo "No remote configured")"
      echo "   Branch: $(git branch --show-current 2>/dev/null || echo "No commits yet")"
      echo "   Status: $(git status --porcelain | wc -l) files changed"
      echo ""
    else
      echo "⚠️  Git not initialized. Run 'git init' to start version control."
      echo ""
    fi
    
    echo "🔧 Setup Instructions:"
    echo "1. Copy config: cp config.env.example config.env"
    echo "2. Edit credentials: nano config.env"
    echo "3. Load environment: source config.env"
    echo "4. Install Python deps: pip install --user -r requirements.txt"
    echo "5. Start ngrok: ngrok http 3000"
    echo "6. Run application: python pydial.py"
    echo ""
    echo "📚 Configuration:"
    echo "   All environment variables are defined in config.env"
    echo "   Make sure to run 'source config.env' before starting the application"
    echo ""
    
    # Load configuration from config.env if it exists
    if [ -f "config.env" ]; then
      echo "🔧 Loading configuration from config.env..."
      source config.env
      echo "✅ Configuration loaded!"
      
      # Set up ngrok authentication if token is available
      if [ -n "$NGROK_AUTHTOKEN" ] && command -v ngrok >/dev/null 2>&1; then
        echo "🔐 Setting up ngrok authentication..."
        ngrok config add-authtoken $NGROK_AUTHTOKEN >/dev/null 2>&1
        echo "✅ ngrok authenticated!"
      fi
    else
      echo "⚠️  config.env not found!"
      echo "   Please create config.env with your SignalWire and Anthropic credentials"
      echo "   See README for setup instructions"
    fi
    
    echo "🌐 ngrok available: $(which ngrok 2>/dev/null && echo "✅ Ready" || echo "❌ Not found")"
    
    # Install Python dependencies using --user flag to avoid nix conflicts
    if [ -f "requirements.txt" ]; then
      echo "📦 Installing Python dependencies with --user flag..."
      pip install --user --upgrade pip
      pip install --user -r requirements.txt
      echo "✅ Dependencies should be installed!"
      echo ""
      echo "🌐 Flask version: $(python -c "import flask; print(flask.__version__)" 2>/dev/null || echo "Not installed")"
      echo "📞 SignalWire version: $(python -c "import signalwire; print(signalwire.__version__)" 2>/dev/null || echo "Not installed")"
      echo "🤖 Anthropic version: $(python -c "import anthropic; print(anthropic.__version__)" 2>/dev/null || echo "Not installed")"
    fi
    
    echo "🚀 Ready to make AI-powered phone calls!"
    echo ""
  '';
  
  # Environment variables that should be set
  NIX_SHELL_PRESERVE_PROMPT = 1;
} 