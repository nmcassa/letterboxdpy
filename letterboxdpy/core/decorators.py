from functools import wraps

# -- DECORATORS --

def assert_instance(expected_class):
    """Ensures the argument passed is an instance of a specified class."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            """
            Verifies if the argument is an instance of the expected class.

            Args:
                instance: Object to check if it's an instance of the expected class.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                The result of the decorated function.

            Raises:
                AssertionError: If the instance is not of the expected class.
            """
            if not isinstance(instance, expected_class):
                raise AssertionError(f"Argument {instance} is not an instance of {expected_class.__name__}")
            return func(instance, *args, **kwargs)

        return wrapper

    return decorator


if __name__ == "__main__":

    @assert_instance(int)
    def printint(arg: int):
        print(arg)

    try:
        printint(1)
        printint("2")
    except AssertionError as e:
        print(e)
