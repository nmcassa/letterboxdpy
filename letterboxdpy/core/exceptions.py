class PageFetchError(Exception):
    """Custom exception for errors related to fetching pages."""

    pass


class PageLoadError(Exception):
    """Raised when loading a page from a given URL fails."""

    def __init__(self, url, message="Failed to load the page"):
        super().__init__(f"{message}: {url}")
        self.url = url


class InvalidResponseError(Exception):
    """Exception raised when an HTTP response is invalid or unexpected."""

    def __init__(self, message: str, code: int | None = None):
        super().__init__(message)
        self.message = message
        self.code = code


class ResourceNotFoundError(Exception):
    """Raised when a requested resource (URL) cannot be found (404)."""

    def __init__(self, url: str, message: str = "Resource not found"):
        super().__init__(f"{message}: {url}")
        self.url = url


class MovieNotFoundError(ResourceNotFoundError):
    """Raised when a movie cannot be found for a given slug or ID."""

    def __init__(self, identifier: str, url: str):
        super().__init__(url, message=f"Movie not found (slug/id: {identifier})")
        self.identifier = identifier


class CustomEncoderError(Exception):
    """Custom error class to represent errors that occur during encoding."""

    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self):
        return f"CustomEncoderError: {self.message}"


class PrivateRouteError(Exception):
    """Exception raised when a private route is accessed."""

    pass


class AccessDeniedError(Exception):
    """Exception raised when access is denied by the server (e.g. IP/VPN block)."""

    def __init__(self, message: str = "Access Denied"):
        self.message = message
        hint = "\nHint: If you are using a VPN or Proxy, Letterboxd might be blocking your connection. Try disabling it."
        super().__init__(f"{message}{hint}")


# ----------------
# Auth Exceptions
# ----------------


class AuthError(Exception):
    """Base class for all authentication-related errors."""

    pass


class LoginFailedError(AuthError):
    """Raised when login attempt fails (e.g. invalid credentials)."""

    pass


class SessionError(AuthError):
    """Raised when session is invalid, expired, or missing required cookies."""

    pass


class MissingCredentialsError(AuthError):
    """Raised when username/password are required but not provided."""

    pass
