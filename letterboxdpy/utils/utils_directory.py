import os


class Directory:
    """Utility class for directory operations."""
    
    @staticmethod
    def exists(path: str) -> bool:
        """Check if directory exists."""
        return os.path.isdir(path)
    
    @staticmethod
    def create(path: str, silent: bool = False) -> bool:
        """Create directory if it doesn't exist. Returns True if created."""
        try:
            if not os.path.exists(path):
                if not silent:
                    print(f'Directory created: {path}')
                os.makedirs(path, exist_ok=True)
                return True
            
            if not silent:
                print(f'Directory found: {path}')
            return False
        except OSError as e:
            if not silent:
                print(f"Error creating {path}: {e}")
            return False
    
    @staticmethod
    def delete(path: str) -> bool:
        """Delete empty directory. Returns True if deleted."""
        if os.path.isdir(path):
            os.rmdir(path)
            return True
        return False
    
    @staticmethod
    def list(path: str) -> list:
        """List contents of directory."""
        if os.path.isdir(path):
            return os.listdir(path)
        return []
    
    @staticmethod
    def check(*paths: str) -> None:
        """Check and create multiple directories. Prints status for each."""
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                print(f'Directory created: {path}')
            else:
                print(f'Directory found: {path}')


def check_and_create_dirs(directories: list | str) -> None:
    """Checks if directories exist, creates them if not."""
    if isinstance(directories, str):
        directories = [directories]

    print('\nChecking directories...')
    for directory in directories:
        Directory.create(directory)
    print('All directories checked, continuing...', end='\n\n')
