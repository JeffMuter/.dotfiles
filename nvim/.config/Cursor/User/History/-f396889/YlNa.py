#!/usr/bin/env python3
from rich.console import Console
from menu import make_call_menu
from menu.utils import console, print_header
from signalwire import SignalWireClient
import os

def make_call(call_details):
    """
    Make an AI phone call using SignalWire.
    """
    console.print("\n[success]📱 Preparing AI call...[/success]")
    console.print(f"Calling: [bold]{call_details.phone_number}[/bold]")
    console.print(f"Contact: [bold]{call_details.contact_name}[/bold]")
    console.print(f"Objective: [bold]{call_details.objective}[/bold]")
    if call_details.additional_context:
        console.print(f"Additional Context: [bold]{call_details.additional_context}[/bold]")
    
    try:
        # Get API key from environment
        api_key = os.environ.get("SIGNALWIRE_API_KEY")
        if not api_key:
            console.print("[error]Error: SIGNALWIRE_API_KEY environment variable not set[/error]")
            return
            
        # Initialize SignalWire client
        console.print("[info]Initializing SignalWire client...[/info]")
        client = SignalWireClient(api_key=api_key)
        
        console.print("[info]Initiating call...[/info]")
        response = client.make_call(call_details)
        
        console.print("\n[success]🤖 Call initiated successfully![/success]")
        console.print(f"[bold cyan]Call ID: {response.get('id', 'Unknown')}[/bold cyan]")
        
    except ImportError as e:
        console.print(f"\n[error]Error: Missing required dependencies. Please run 'pip install -r requirements.txt'\nDetails: {str(e)}[/error]")
        return
    except Exception as e:
        console.print(f"\n[error]Error initiating call: {str(e)}[/error]")
        return

def main():
    """Main entry point."""
    try:
        print_header("Welcome to PyDial!")
        console.print("Your AI-powered calling assistant\n")
        
        # Get call details from the menu
        call_details = make_call_menu()
        
        # Make the call
        make_call(call_details)
        
    except KeyboardInterrupt:
        console.print("\n[error]Operation cancelled by user[/error]")
        return 1
    except Exception as e:
        console.print(f"\n[error]An error occurred: {str(e)}[/error]")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 