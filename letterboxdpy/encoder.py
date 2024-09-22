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