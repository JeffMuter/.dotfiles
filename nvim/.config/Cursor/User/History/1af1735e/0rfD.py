#!/usr/bin/env python3
"""
Entry point for PyDial web interface.
"""
from web import create_app

def main():
    """Run the web interface."""
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main() 