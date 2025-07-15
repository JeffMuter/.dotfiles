{ pkgs ? import <nixpkgs> { config = { allowUnfree = true; }; } }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    ngrok
    (python3.withPackages (ps: with ps; [
      python-dotenv
      rich
      typer
      pydantic
      pytest
      pytest-mock
      transformers
      torch
      accelerate
      anthropic
      requests
      flask
      sqlalchemy
      werkzeug
      flask-login
      flask-wtf
      email-validator
      flask-sqlalchemy
      pip
    ]))
  ];
  
  # Environment variables
  shellHook = ''
    # Install signalwire-python if not already installed
    pip install --user signalwire

    export ANTHROPIC_API_KEY="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"
    export SIGNALWIRE_API_KEY="PTdf9d22445677bb1f81962e7c14d907d6671d6eeff891f476"
    export TARGET_PHONE_NUMBER="16145572867"
    export SIGNALWIRE_PHONE_NUMBER="16144126309"  # Replace with your actual SignalWire phone number
    export SIGNALWIRE_PROJECT_ID="8cbde92d-5678-43ed-8c37-e56551820972"
    export SIGNALWIRE_VOICE_GENDER="female"  # Options: female, male
    export SIGNALWIRE_VOICE_LOCALE="en-US"  # Options: en-US, en-GB, en-AU
    export SIGNALWIRE_SPACE_NAME="saorsadev"
    export NGROK_API_KEY="2xUu328LKTtLJ8LeYDW4i3J6r8g_7KDyw9tey5bRVv6F4mYo7"

    # Function to start webhook server and ngrok
    start_servers() {
      # Kill any existing ngrok processes
      pkill -f ngrok || true
      
      # Start the Flask server in the background
      python signalwire/webhook_server.py &
      FLASK_PID=$!
      
      # Wait a moment for Flask to start
      sleep 2
      
      # Start ngrok and get the public URL
      ngrok authtoken $NGROK_API_KEY
      ngrok http 5000 > ngrok.log 2>&1 &
      NGROK_PID=$!
      
      # Wait for ngrok to generate the URL
      sleep 5
      
      # Extract and export the ngrok URL
      export WEBHOOK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | grep -o 'http[^"]*')/ai-agent
      echo "Webhook URL: $WEBHOOK_URL"
      
      # Save PIDs for cleanup
      echo $FLASK_PID > .flask.pid
      echo $NGROK_PID > .ngrok.pid
    }

    # Function to stop servers
    stop_servers() {
      [ -f .flask.pid ] && kill $(cat .flask.pid) 2>/dev/null || true
      [ -f .ngrok.pid ] && kill $(cat .ngrok.pid) 2>/dev/null || true
      rm -f .flask.pid .ngrok.pid
      pkill -f ngrok || true
    }
    
    echo "Welcome to pyDial!"
    echo "Choose an application to run:"
    echo "1) Phone Call Application (main.py)"
    echo "2) Web Interface (run_web.py)"
    echo "3) Just enter shell"
    
    read -p "Enter your choice (1-3): " choice
    
    case $choice in
      1)
        echo "Starting phone call application..."
        # Start servers before running main.py
        echo "Starting webhook server and ngrok..."
        start_servers
        python main.py
        stop_servers
        ;;
      2)
        echo "Starting web interface..."
        python run_web.py
        ;;
      3)
        echo "Entering shell..."
        ;;
      *)
        echo "Invalid choice. Entering shell..."
        ;;
    esac

    # Cleanup on exit
    trap stop_servers EXIT
  '';
} 