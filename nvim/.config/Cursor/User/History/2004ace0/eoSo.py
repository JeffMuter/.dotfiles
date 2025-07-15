from typing import Optional
from dataclasses import dataclass
from rich.console import Console
from rich.prompt import Prompt, Confirm
from .utils import console, print_header, print_divider
import re

@dataclass
class CallDetails:
    phone_number: str
    contact_name: str
    objective: str
    caller_name: str
    additional_context: Optional[str] = None

def validate_phone_number(number: str) -> str:
    """
    Validate and format phone number to E.164 format.
    Returns formatted number or raises ValueError if invalid.
    """
    # Remove any non-digit characters
    digits = re.sub(r'\D', '', number)
    
    # Check length
    if len(digits) < 10 or len(digits) > 15:
        raise ValueError("Phone number must be between 10 and 15 digits")
    
    # If it's a US/Canada number (10 digits), add +1
    if len(digits) == 10:
        return f"+1{digits}"
    
    # Otherwise just add + prefix
    return f"+{digits}"

def make_call_menu() -> CallDetails:
    """
    Interactive menu to collect call details from the user.
    Returns a CallDetails object with all the necessary information.
    """
    print_header("📞 PyDial Call Setup")
    print_divider()
    
    # Collect call information
    caller_name = Prompt.ask("\n[info]Enter your name (this is who you'll be calling as)[/info]")
    
    # Phone number with validation
    while True:
        try:
            phone_input = Prompt.ask("[info]Enter the phone number to call (10+ digits)[/info]")
            phone_number = validate_phone_number(phone_input)
            break
        except ValueError as e:
            console.print(f"[error]Invalid phone number: {str(e)}[/error]")
    
    contact_name = Prompt.ask("[info]Enter the name of the person/business you're calling[/info]")
    objective = Prompt.ask("[info]What's the objective of this call?[/info]")
    additional_context = Prompt.ask(
        "[info]Any additional context for the AI? (Press Enter to skip)[/info]",
        default=""
    )

    # Create call details
    call_details = CallDetails(
        phone_number=phone_number,
        contact_name=contact_name,
        objective=objective,
        caller_name=caller_name,
        additional_context=additional_context if additional_context else None
    )
    
    # Show summary and confirm
    print_divider()
    console.print("\n[bold]Call Summary:[/bold]")
    console.print(f"From: [cyan]{caller_name}[/cyan]")
    console.print(f"To: [cyan]{phone_number}[/cyan] ({contact_name})")
    console.print(f"Objective: [cyan]{objective}[/cyan]")
    if additional_context:
        console.print(f"Additional Context: [cyan]{additional_context}[/cyan]")
    print_divider()
    
    if not Confirm.ask("\nWould you like to proceed with this call?"):
        console.print("\n[warning]Call cancelled by user[/warning]")
        raise KeyboardInterrupt()
    
    return call_details 