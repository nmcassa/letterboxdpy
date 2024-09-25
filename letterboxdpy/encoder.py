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
    """JSON encoder that excludes specified attributes from the output."""
    
    def __init__(self, excl_attrs: list=['secrets'], **kwargs):
        assert isinstance(excl_attrs, list), "excl_attrs must be a list"
        assert len(excl_attrs) > 0, "excl_attrs must not be empty"
        assert all(isinstance(attr, str) for attr in excl_attrs), "All elements in excl_attrs must be strings"
        self.excl_attrs = set(excl_attrs)
        super().__init__(**kwargs)

    def default(self, o):
        """Encodes the object to JSON format excluding specified attributes."""
        try:
            obj_copy = {k: v for k, v in o.__dict__.items() if k not in self.excl_attrs}
        except AttributeError as e:
            raise CustomEncoderError(f"Object of type {type(o).__name__} has no __dict__ attribute") from e
        return obj_copy