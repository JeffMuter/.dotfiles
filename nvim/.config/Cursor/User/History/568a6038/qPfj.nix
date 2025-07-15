{ pkgs ? import <nixpkgs> { config.allowUnfree = true; } }:

let
  # Create a basic Python environment without conflicting packages
  pythonEnv = pkgs.python311.withPackages (ps: with ps; [
    pip
    setuptools
    wheel
    virtualenv
  ]);
in

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Basic Python with pip
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
    
    # Create and activate virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
      echo "🔧 Creating Python virtual environment..."
      python -m venv venv
      echo "✅ Virtual environment created!"
    fi
    
    # Activate virtual environment only if not already activated
    if [[ "$VIRTUAL_ENV" != *"venv"* ]]; then
      echo "🔧 Activating virtual environment..."
      source venv/bin/activate
      echo "✅ Virtual environment activated!"
      echo "🐍 Using Python: $(which python)"
    else
      echo "✅ Virtual environment already active!"
    fi
    
    # Upgrade pip in virtual environment
    echo "📦 Upgrading pip..."
    pip install --upgrade pip >/dev/null 2>&1
    
    # Install Python dependencies in virtual environment
    if [ -f "requirements.txt" ]; then
      echo "📦 Installing Python dependencies..."
      pip install -r requirements.txt >/dev/null 2>&1
      echo "✅ Dependencies installed!"
      echo ""
      echo "🌐 Flask version: $(python -c "import flask; print(flask.__version__)" 2>/dev/null || echo "Not installed")"
      echo "📞 SignalWire version: $(python -c "import signalwire; print(signalwire.__version__)" 2>/dev/null || echo "Not installed")"
      echo "🤖 Anthropic version: $(python -c "import anthropic; print(anthropic.__version__)" 2>/dev/null || echo "Not installed")"
    fi
    
    echo ""
    echo "🔧 Setup Instructions:"
    echo "1. Copy config: cp config.env.example config.env"
    echo "2. Edit credentials: nano config.env"
    echo "3. Load environment: source config.env"
    echo "4. Start ngrok: ngrok http 3000"
    echo "5. Run application: python pydial.py"
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
    echo "🚀 Ready to make AI-powered phone calls!"
    echo ""
  '';
  
  # Environment variables that should be set
  NIX_SHELL_PRESERVE_PROMPT = 1;
} 