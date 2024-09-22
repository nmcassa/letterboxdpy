from json import JSONEncoder
from letterboxdpy.exceptions import CustomEncoderError


class Encoder(JSONEncoder):
    """
    Encoder class provides a way to serialize custom class
    .. instances to JSON by overriding the default serialization
    .. logic to return the object's namespace dictionary.
    """
    def default(self, o):
        if not hasattr(o, '__dict__'):
            raise CustomEncoderError(f"Object of type {type(o).__name__} has no __dict__ attribute")
        
        try:
            return o.__dict__
        except Exception as e:
            raise CustomEncoderError("An error occurred during encoding") from e
    
class SecretsEncoder(JSONEncoder):
    """JSON encoder that excludes the 'secrets' attribute from the output."""
    
    def default(self, o):
        try:
            if hasattr(o, 'secrets'):
                o_copy = o.__dict__.copy()
                o_copy.pop('secrets', None)
                return o_copy
            else:
                raise TypeError(f"'{self.__class__.__name__}' can only encode objects with a 'secrets' attribute.")
        except Exception as e:
            raise CustomEncoderError("An error occurred while encoding") from e