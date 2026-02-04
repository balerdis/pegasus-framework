# pegasus_framework/auth/exceptions/invalid_token.py

from .authentication_error import AuthenticationError

class InvalidTokenError(AuthenticationError):
    def __init__(self, message: str | None = None):
        super().__init__(message)