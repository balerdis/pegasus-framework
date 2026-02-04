# pegasus_framework/auth/exceptions/authentication_error.py

class AuthenticationError(Exception):
    """Base class for authentication-related errors."""
    def __init__(self, message: str | None = None):
        super().__init__(message)