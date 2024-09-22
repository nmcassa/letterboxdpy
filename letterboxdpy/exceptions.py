class CustomEncoderError(Exception):
    """Custom error class to represent errors that occur during encoding."""
    
    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self):
        return f"CustomEncoderError: {self.message}"