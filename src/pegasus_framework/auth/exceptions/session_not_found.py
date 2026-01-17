# pegasus_framework/auth/exceptions/session_not_found.py

from .authentication_error import AuthenticationError

class SessionNotFoundError(AuthenticationError):
    pass