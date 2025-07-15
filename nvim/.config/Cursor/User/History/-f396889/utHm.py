#!/usr/bin/env python3
from rich.console import Console
from menu import make_call_menu

console = Console()

def make_call(call_details):
    """
    Placeholder for the actual call implementation.
    This will be implemented later with the actual calling functionality.
    """
    console.print("\n[bold green]📱 Initiating call...[/bold green]")
    console.print(f"Calling: [bold]{call_details.phone_number}[/bold]")
    console.print(f"Contact: [bold]{call_details.contact_name}[/bold]")
    console.print(f"Objective: [bold]{call_details.objective}[/bold]")
    if call_details.additional_context:
        console.print(f"Additional Context: [bold]{call_details.additional_context}[/bold]")
    
    # TODO: Implement actual calling functionality
    console.print("\n[yellow]Note: Actual calling functionality will be implemented in future updates[/yellow]")

def main():
    try:
        console.print("[bold blue]Welcome to PyDial![/bold blue]")
        console.print("Your AI-powered calling assistant\n")
        
        # Get call details from the menu
        call_details = make_call_menu()
        
        # Make the call
        make_call(call_details)
        
    except KeyboardInterrupt:
        console.print("\n[red]Operation cancelled by user[/red]")
        return 1
    except Exception as e:
        console.print(f"\n[red]An error occurred: {str(e)}[/red]")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 