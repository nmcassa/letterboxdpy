import os
from json import (
    dump as json_dump,
    load as json_load,
    loads as json_loads,
    dumps as json_dumps
)


class File:
    """Base utility class for file operations."""
    EXTENSION = ''
    
    @classmethod
    def _get_path(cls, path: str) -> str:
        """Get full path with extension."""
        if cls.EXTENSION and not path.endswith(cls.EXTENSION):
            return f'{path}{cls.EXTENSION}'
        return path
    
    @classmethod
    def exists(cls, path: str) -> bool:
        """Check if file exists."""
        return os.path.exists(cls._get_path(path))
    
    @classmethod
    def delete(cls, path: str) -> bool:
        """Delete file if exists. Returns True if deleted."""
        filepath = cls._get_path(path)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    @staticmethod
    def save(path: str, data: dict, format: str = 'json') -> None:
        """Save data to file in the specified format."""
        if format == 'json':
            JsonFile.save(path, data)
        else:
            raise ValueError(f"Unsupported format '{format}'. Only 'json' is currently supported.")


class JsonFile(File):
    """Utility class for JSON file operations."""
    EXTENSION = '.json'
    
    @classmethod
    def save(cls, path: str, data: dict | list, indent: int = 2) -> None:
        """Save data to a JSON file."""
        with open(cls._get_path(path), 'w') as f:
            json_dump(data, f, indent=indent)
    
    @classmethod
    def load(cls, path: str) -> dict | None:
        """Load data from a JSON file. Returns None if file doesn't exist."""
        filepath = cls._get_path(path)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json_load(f)
        return None
    
    @staticmethod
    def parse(text: str) -> dict | None:
        """Parse JSON from string. Returns None if parsing fails."""
        try:
            return json_loads(text)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def stringify(data, indent: int = None, encoder=None, **kwargs) -> str:
        """Convert dict to JSON string. Supports custom encoder and extra args."""
        return json_dumps(data, indent=indent, cls=encoder, **kwargs)


class CsvFile(File):
    """Utility class for CSV file operations."""
    EXTENSION = '.csv'
    
    @classmethod
    def save(cls, path: str, rows: list, headers: list = None) -> None:
        """Save rows to a CSV file. First row can be headers."""
        import csv
        with open(cls._get_path(path), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if headers:
                writer.writerow(headers)
            writer.writerows(rows)
    
    @classmethod
    def load(cls, path: str) -> list | None:
        """Load rows from a CSV file. Returns None if file doesn't exist."""
        import csv
        filepath = cls._get_path(path)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return list(csv.reader(f))
        return None


class BinaryFile(File):
    """Utility class for binary file operations (images, etc)."""
    EXTENSION = ''
    
    @classmethod
    def save(cls, path: str, data: bytes) -> None:
        """Save binary data to file."""
        with open(cls._get_path(path), 'wb') as f:
            f.write(data)
    
    @classmethod
    def load(cls, path: str) -> bytes | None:
        """Load binary data from file. Returns None if file doesn't exist."""
        filepath = cls._get_path(path)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                return f.read()
        return None


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
