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
        Badge status is lazily evaluated on first access and cached on `self._badge` directly
        by this decorator. This keeps page classes (e.g. UserProfile) clean and focused on
        DOM extraction without coupling them to intermediate caching state.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Check cached badge on the instance to avoid redundant DOM lookups
            badge = getattr(self, "_badge", None)
            if badge is None:
                if hasattr(self, "get_badge"):
                    badge = self.get_badge()
                else:
                    badge = getattr(self, "badge", None)
                self._badge = badge

            if badge == "hq":
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
