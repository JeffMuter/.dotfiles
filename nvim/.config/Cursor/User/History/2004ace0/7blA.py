from typing import Optional
from dataclasses import dataclass
from rich.console import Console
from rich.prompt import Prompt

console = Console()

@dataclass
class CallDetails:
    phone_number: str
    contact_name: str
    objective: str
    additional_context: Optional[str] = None

def make_call_menu() -> CallDetails:
    """
    Interactive menu to collect call details from the user.
    Returns a CallDetails object with all the necessary information.
    """
    console.print("\n[bold blue]📞 PyDial Call Setup[/bold blue]")
    console.print("=" * 50)
    
    # Collect call information
    phone_number = Prompt.ask("\n[cyan]Enter the phone number to call[/cyan]")
    contact_name = Prompt.ask("[cyan]Enter the name of the person/business you're calling[/cyan]")
    objective = Prompt.ask("[cyan]What's the objective of this call?[/cyan]")
    additional_context = Prompt.ask(
        "[cyan]Any additional context for the AI? (Press Enter to skip)[/cyan]",
        default=""
    )

    # Create and return call details
    return CallDetails(
        phone_number=phone_number,
        contact_name=contact_name,
        objective=objective,
        additional_context=additional_context if additional_context else None
    ) 