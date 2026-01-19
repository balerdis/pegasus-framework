# pegasus_framework/api/exceptions/handlers/auth/authentication_failed.py

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pegasus_framework.api.v1.schemas.generic import ErrorResponse

async def authentication_failed_handler(
    request: Request,
    exc: Exception,
):
    payload = ErrorResponse(
        success=False,
        message="Token inválido o sesión expirada",
        error_code="INVALID_TOKEN_OR_SESSION",
        details=None,
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=payload,
        headers={"WWW-Authenticate": "Bearer"},
    )
