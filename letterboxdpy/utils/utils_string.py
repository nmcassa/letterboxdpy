def remove_prefix(text: str, prefix: str) -> str:
    """Remove a specific prefix from a string if it exists."""
    return text[len(prefix):] if text.startswith(prefix) else text

def strip_prefix(method_name: str, prefix: str = 'get_') -> str:
    """Remove the 'get_' prefix from a method name if it exists."""
    return remove_prefix(method_name, prefix)
