from functools import wraps

# -- DECORATORS --


def assert_instance(expected_class: type):
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
                raise AssertionError(
                    f"Argument {instance} is not an instance of {expected_class.__name__}"
                )
            return func(instance, *args, **kwargs)

        return wrapper

    return decorator


def skip_if_hq(default=None):
    """
    Decorator to skip method execution and return a default value if the instance is an HQ account.

    Note on caching:
        HQ status is lazily evaluated on first access and cached on `self._is_hq` directly
        by this decorator. This keeps page classes (e.g. UserProfile) clean and focused on
        DOM extraction without coupling them to intermediate caching state.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Check cached HQ status on the instance to avoid redundant DOM lookups
            is_hq = getattr(self, "_is_hq", None)
            if is_hq is None:
                if hasattr(self, "get_hq_status"):
                    is_hq = self.get_hq_status()
                else:
                    is_hq = getattr(self, "is_hq", False)
                self._is_hq = is_hq

            if is_hq:
                return default
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


if __name__ == "__main__":

    @assert_instance(int)
    def printint(arg: int):
        print(arg)

    try:
        printint(1)
        printint("2")  # type: ignore
    except AssertionError as e:
        print(e)
