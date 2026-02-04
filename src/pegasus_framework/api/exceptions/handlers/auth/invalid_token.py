# pegasus_framework/api/exceptions/handlers/auth/invalid_token.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from pegasus_framework.api.v1.schemas.generic import ErrorResponse
from pegasus_framework.auth.exceptions import InvalidTokenError


async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenError,
):
    message = str(exc) if str(exc) else "Invalid or expired token"

    payload = ErrorResponse(
        success=False,
        message=message,
        error_code="INVALID_TOKEN",
        details=None,
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=payload,
        headers={"WWW-Authenticate": "Bearer"},
    )
