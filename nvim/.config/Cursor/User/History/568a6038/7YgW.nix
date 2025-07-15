{ pkgs ? import <nixpkgs> {} }:

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
    export SIGNALWIRE_SPACE_NAME="https://www.saorsadev.signalwire.com"
    echo "Starting pyDial..."
    python main.py
  '';
} 