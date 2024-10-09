import sys
import os


def get_input(prompt: str, *, index: int = None, expected_type: type = str) -> any:
    """"Retrieve value from command-line argument or prompt user for input."""
    def convert(value):
        return expected_type(value)

    if index:
        try:
            return convert(sys.argv[index])
        except (IndexError, ValueError):
            pass

    while True:
        try:
            value = input(prompt).strip()
            if value:
                return convert(value)
        except ValueError:
            pass
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Exiting...")
            sys.exit(0)

def args_exists() -> bool:
    """Check if command-line arguments exist."""
    return len(sys.argv) > 1

# CORE

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