from json import JSONEncoder
from enum import Enum
from letterboxdpy.core.exceptions import CustomEncoderError


class Encoder(JSONEncoder):
    """
    Encoder class provides a way to serialize custom class
    .. instances to JSON by overriding the default serialization
    .. logic to return the object's namespace dictionary.
    """
    def default(self, o):
        if isinstance(o, Enum):
            return o.value
        
        try:
            return o.__dict__
        except AttributeError:
            return super().default(o)
        except Exception as e:
            raise CustomEncoderError(f"An error occurred during encoding: {e}") from e

class SecretsEncoder(JSONEncoder):
    """JSON encoder that excludes specified attributes from the output."""

    def __init__(self, secrets: list = ['secrets'], **kwargs):
        if not isinstance(secrets, list):
            raise TypeError("secrets must be a list")
        if not secrets:
            raise ValueError("secrets must not be empty")
        if not all(isinstance(attr, str) for attr in secrets):
            raise TypeError("All elements in secrets must be strings")

        self.secrets = set(secrets)
        super().__init__(**kwargs)

    def default(self, o):
        """Encodes the object to JSON format excluding specified attributes."""
        if isinstance(o, Enum):
            return o.value
        
        try:
            return {k: v for k, v in o.__dict__.items() if k not in self.secrets}
        except AttributeError:
            return super().default(o)
        except Exception as e:
            raise CustomEncoderError(f"An error occurred during encoding: {e}") from e
