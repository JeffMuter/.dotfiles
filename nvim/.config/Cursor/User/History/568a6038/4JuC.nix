{ pkgs ? import <nixpkgs> { config = { allowUnfree = true; }; } }:

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
      sqlalchemy
      werkzeug
      flask-login
      flask-wtf
      email-validator
      flask-sqlalchemy
    ]))
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
    
    echo "Welcome to pyDial!"
    echo "Choose an application to run:"
    echo "1) Phone Call Application (main.py)"
    echo "2) Web Interface (run_web.py)"
    echo "3) Just enter shell"
    
    read -p "Enter your choice (1-3): " choice
    
    case $choice in
      1)
        echo "Starting phone call application..."
        python main.py
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
  '';
} 