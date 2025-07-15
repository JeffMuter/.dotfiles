from typing import Optional
from dataclasses import dataclass
from rich.console import Console
from rich.prompt import Prompt
from .utils import console, print_header, print_divider

@dataclass
class CallDetails:
    phone_number: str
    contact_name: str
    objective: str
    caller_name: str
    additional_context: Optional[str] = None

def make_call_menu() -> CallDetails:
    """
    Interactive menu to collect call details from the user.
    Returns a CallDetails object with all the necessary information.
    """
    print_header("📞 PyDial Call Setup")
    print_divider()
    
    # Collect call information
    caller_name = Prompt.ask("\n[info]Enter your name (this is who you'll be calling as)[/info]")
    phone_number = Prompt.ask("[info]Enter the phone number to call[/info]")
    contact_name = Prompt.ask("[info]Enter the name of the person/business you're calling[/info]")
    objective = Prompt.ask("[info]What's the objective of this call?[/info]")
    additional_context = Prompt.ask(
        "[info]Any additional context for the AI? (Press Enter to skip)[/info]",
        default=""
    )

    # Create and return call details
    return CallDetails(
        phone_number=phone_number,
        contact_name=contact_name,
        objective=objective,
        caller_name=caller_name,
        additional_context=additional_context if additional_context else None
    ) 