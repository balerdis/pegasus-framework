from fastapi import FastAPI
from pegasus_framework.auth.exceptions.invalid_token import InvalidTokenError
from pegasus_framework.auth.exceptions.session_not_found import SessionNotFoundError

from .handlers.auth.invalid_token import invalid_token_handler
from .handlers.auth.session_not_found import session_not_found_handler


def register_auth_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        InvalidTokenError,
        invalid_token_handler,
    )

    app.add_exception_handler(
        SessionNotFoundError,
        session_not_found_handler,
    )
