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
    ]))
  ];
  
  # Environment variables
  shellHook = ''
    export ANTHROPIC_API_KEY="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"  # Replace with your actual key
    export SIGNALWIRE_API_KEY="PTdf9d22445677bb1f81962e7c14d907d6671d6eeff891f476"
    echo "Starting pyDial..."
    python main.py
  '';
} 