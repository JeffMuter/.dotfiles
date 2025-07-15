from rich.console import Console
from rich.theme import Theme

# Create a custom theme for consistent styling
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "header": "bold blue",
})

# Create a single console instance to be shared across the application
console = Console(theme=custom_theme)

# Common styling functions
def print_header(text: str) -> None:
    """Print a formatted header."""
    console.print(f"\n[header]{text}[/header]")

def print_divider() -> None:
    """Print a divider line."""
    console.print("=" * 50) 