# pegasus_framework/auth/exceptions/invalid_token.py

from .authentication_error import AuthenticationError

class InvalidTokenError(AuthenticationError):
    pass