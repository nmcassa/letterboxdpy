import os
from json import dump as json_dump
from typing import Union


def save_data(path: str, data: dict, format: str = 'json') -> None:
    """Save data to a file in the specified format."""
    if format == 'json':
        save_json(path, data)
    else:
        raise ValueError(f"Unsupported format '{format}'. Only 'json' is currently supported.")

def check_and_create_dirs(directories: Union[list, str]) -> None:
    """Checks if directories exist, creates them if not."""
    if isinstance(directories, str):
        directories = [directories]

    print('\nChecking directories...')
    for directory in directories:
        create_directory(directory)
    print('\tAll directories checked, continuing...', end='\n\n')

def save_json(path: str, data: dict) -> None:
    """Save data to a file as JSON."""
    with open(f'{path}.json', 'w') as f:
        json_dump(data, f, indent=2)

def create_directory(directory: str) -> None:
    """Creates a directory if it does not exist."""
    try:
        if not os.path.exists(directory):
            print(f'\tCreating {directory}')
            os.makedirs(directory, exist_ok=True)
        else:
            print(f'\tFound {directory}')
    except OSError as e:
        print(f"\tError creating {directory}: {e}")

def build_path(*segments: str, normalize: bool = True) -> str:
    """Build and format file paths from the given segments."""
    path = os.path.join(*segments)
    if normalize:
        return os.path.normpath(path)
    return path

def build_click_url(file_path: str, protocol: str = 'file') -> str:
    """Build a clickable file URL with the specified protocol."""
    if protocol == 'file':
        return f"file:///{build_path(os.getcwd(), file_path).replace(os.sep, '/')}"
    elif protocol in ['http', 'https']:
        return f"{protocol}://{file_path}"
    else:
        raise ValueError(f"Unsupported protocol '{protocol}'")