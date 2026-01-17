from fastapi import Request, status
from fastapi.responses import JSONResponse
from pegasus_framework.api.v1.schemas.generic import ErrorResponse
from pegasus_framework.auth.exceptions import InvalidTokenError


async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenError,
):
    payload = ErrorResponse(
        success=False,
        message="Invalid or expired token",
        error_code="INVALID_TOKEN",
        details=None,
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=payload,
        headers={"WWW-Authenticate": "Bearer"},
    )
