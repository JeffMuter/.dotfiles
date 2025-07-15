#!/usr/bin/env python3
from rich.console import Console
from menu import make_call_menu
from menu.utils import console, print_header
from inference import TinyLlamaModel

def make_call(call_details):
    """
    Generate AI response based on call details and eventually make the call.
    """
    console.print("\n[success]📱 Preparing AI response...[/success]")
    console.print(f"Calling: [bold]{call_details.phone_number}[/bold]")
    console.print(f"Contact: [bold]{call_details.contact_name}[/bold]")
    console.print(f"Objective: [bold]{call_details.objective}[/bold]")
    if call_details.additional_context:
        console.print(f"Additional Context: [bold]{call_details.additional_context}[/bold]")
    
    # Create the prompt for the AI
    prompt = f"""
    You need to make a phone call to {call_details.contact_name} at {call_details.phone_number}.
    Your objective is: {call_details.objective}
    """
    if call_details.additional_context:
        prompt += f"\nAdditional context: {call_details.additional_context}"
    
    try:
        # Initialize and use the LLM
        console.print("[info]Loading AI model...[/info]")
        llm = TinyLlamaModel()
        
        console.print("[info]Generating response...[/info]")
        response = llm.generate_response(prompt)
        
        if not response or response.strip() == "":
            console.print("\n[error]Error: Generated response was empty[/error]")
            return
            
        console.print("\n[success]🤖 AI Response Generated:[/success]")
        console.print(f"[bold cyan]{response}[/bold cyan]")
        
    except ImportError as e:
        console.print(f"\n[error]Error: Missing required dependencies. Please run 'pip install -r requirements.txt'\nDetails: {str(e)}[/error]")
        return
    except Exception as e:
        console.print(f"\n[error]Error generating AI response: {str(e)}[/error]")
        return
    
    # TODO: Implement actual calling functionality
    console.print("\n[warning]Note: Actual calling functionality will be implemented in future updates[/warning]")

def main():
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