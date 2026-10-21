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


_DEFAULT_MATCH = object()
_MISSING = object()


def skip_if(target, match=_DEFAULT_MATCH, default=None):
    """
    Decorator to skip method execution and return `default` if a condition or match is met.

    Evaluates the target attribute, method, or callable on the instance lazily.
    The resolved value is cached on `self._{target}` so that repeated checks
    (across multiple decorated methods) execute the underlying getter or DOM
    lookup only once per instance.

    Args:
        target: Attribute or method name (str) on the instance, or a callable predicate(self).
                If a string like 'badge' is provided, it automatically checks 'self.badge'
                and falls back to 'self.get_badge()'.
        match: Value or container (tuple/list/set/frozenset) of values to compare against.
               If omitted, skips whenever the target resolves to truthy (boolean flag).
        default: Return value when skipped (default is None).

    Supported Scenarios & Usage Examples:
        1. Single Value Match (Attribute/Method):
           @skip_if("badge", "hq", default=None)
           Skips if self.badge == "hq" (or self.get_badge() == "hq").

        2. Container / Multi-Value Match:
           @skip_if("badge", (None, "pro"), default=None)
           Skips if the resolved badge is in the provided tuple/list/set.

        3. Boolean Flag (Omitted match):
           @skip_if("is_private", default=None)
           Skips if self.is_private (or self.get_is_private()) evaluates to True.

        4. Method Name (Direct):
           @skip_if("get_status", "maintenance")
           Skips if self.get_status() == "maintenance".

        5. Explicit None Match:
           @skip_if("website", match=None)
           Skips if self.website is None.

        6. Custom Callable Predicate:
           @skip_if(lambda self: self.year < 1900, default="TOO_OLD")
           Skips if the callable predicate returns True for self.
    """

    is_callable = callable(target)
    cache_attr = f"_{target}" if isinstance(target, str) else None
    getter_fallback = (
        f"get_{target}"
        if isinstance(target, str) and not target.startswith("get_")
        else None
    )
    has_match = match is not _DEFAULT_MATCH
    is_container = isinstance(match, tuple | list | set | frozenset)
    match_container = set(match) if is_container else None

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if is_callable:
                should_skip = bool(target(self))
            elif cache_attr:
                try:
                    val = getattr(self, cache_attr)
                except AttributeError:
                    attr = getattr(self, target, _MISSING)
                    if attr is _MISSING and getter_fallback:
                        attr = getattr(self, getter_fallback, _MISSING)
                    if attr is _MISSING:
                        attr = None
                    val = attr() if callable(attr) else attr
                    setattr(self, cache_attr, val)

                if has_match:
                    should_skip = (
                        val in match_container if is_container else (val == match)
                    )
                else:
                    should_skip = bool(val)
            else:
                should_skip = False

            if should_skip:
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
