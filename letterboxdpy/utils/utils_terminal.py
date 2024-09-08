import sys
import os


def get_arg(index: int, default: str = None) -> str:
    """Retrieve command-line argument at a given index."""
    if len(sys.argv) > index:
        return sys.argv[index]
    return default

def ask_confirmation(prompt: str = "Do you want to continue? (y/n): ") -> bool:
    """Prompt the user for confirmation and return boolean response."""
    response = input(prompt).lower()
    return response in ['y', 'yes']

def clear_screen() -> None:
    """Clear the terminal screen based on the operating system."""
    os_name = os.name
    if os_name == 'nt':
        os.system('cls')
    elif os_name == 'posix':
        os.system('clear')
    else:
        raise NotImplementedError("Unsupported operating system")
    
def get_input(prompt: str, *, index: int = None) -> str:
    """Retrieve value from command-line argument or prompt user for input."""
    value = get_arg(index, '') if index else ''
    while not value.strip():
        clear_screen()
        value = input(f"{prompt}: ").strip()
    return value.lower()
