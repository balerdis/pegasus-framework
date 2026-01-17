# pegasus_framework/api/exceptions/handlers/auth/session_not_found.py

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pegasus_framework.auth.exceptions import SessionNotFoundError
from pegasus_framework.api.v1.schemas.generic import ErrorResponse


async def session_not_found_handler(
    request: Request,
    exc: SessionNotFoundError,
):
    
    payload = ErrorResponse(
        success=False,
        message="session not found or session expired",
        error_code="INVALID_SESSION",
        details=None,
    ).model_dump()


    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=payload,
        headers={"WWW-Authenticate": "Bearer"},
    )
