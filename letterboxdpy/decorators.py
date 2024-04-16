from functools import wraps

# -- DECORATORS --

def assert_instance(cls):
    """
    A decorator that ensures the argument passed to the decorated function is an instance of a specified class.

    Args:
        cls: The class type to check against.

    Returns:
        function: A decorator function that performs the instance check.

    Raises:
        AssertionError: If the argument is not an instance of the specified class.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(arg, *args, **kwargs):
            """
            Wrapper function that performs the instance check before calling the decorated function.

            Args:
                arg: The argument to check.
                *args: Additional positional arguments to pass to the decorated function.
                **kwargs: Additional keyword arguments to pass to the decorated function.

            Returns:
                Any: The result of calling the decorated function.

            Raises:
                AssertionError: If the argument is not an instance of the specified class.
            """
            assert isinstance(arg, cls), f"Argument {arg} is not an instance of {cls.__name__}"
            return func(arg, *args, **kwargs)
        return wrapper
    return decorator
