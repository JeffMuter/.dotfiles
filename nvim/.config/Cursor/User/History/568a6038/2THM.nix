{ pkgs ? import <nixpkgs> {} }:

allowUnfree = true;

pkgs.mkShell {
  buildInputs = with pkgs; [
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
      ngrok
    ]))
    ngrok
  ];
  
  # Environment variables
  shellHook = ''
    export ANTHROPIC_API_KEY="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"
    export SIGNALWIRE_API_KEY="PTdf9d22445677bb1f81962e7c14d907d6671d6eeff891f476"
    export TARGET_PHONE_NUMBER="16145572867"
    export SIGNALWIRE_PHONE_NUMBER="16144126309"  # Replace with your actual SignalWire phone number
    export SIGNALWIRE_PROJECT_ID="8cbde92d-5678-43ed-8c37-e56551820972"
    export SIGNALWIRE_VOICE_GENDER="female"  # Options: female, male
    export SIGNALWIRE_VOICE_LOCALE="en-US"  # Options: en-US, en-GB, en-AU
    export SIGNALWIRE_SPACE_NAME="saorsadev"
    
    # Function to check if Flask is already running
    check_flask() {
      if netstat -tln | grep -q :5000; then
        return 0
      else
        return 1
      fi
    }
    
    # Function to check if ngrok is already running
    check_ngrok() {
      if pgrep -x "ngrok" > /dev/null; then
        return 0
      else
        return 1
      fi
    }
    
    # Start Flask server if not already running
    if ! check_flask; then
      echo "Starting Flask server..."
      python signalwire/client.py &
      sleep 2  # Give the server a moment to start
    else
      echo "Flask server is already running on port 5000"
    fi
    
    # Start ngrok if not already running
    if ! check_ngrok; then
      echo "Starting ngrok..."
      ngrok http 5000 &
      sleep 5  # Give ngrok time to establish tunnel
      
      # Get the ngrok URL and set it as an environment variable
      export NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
      echo "Ngrok tunnel established at: $NGROK_URL"
    else
      echo "Ngrok is already running"
    fi
    
    echo "Starting pyDial..."
    python main.py
  '';
} 