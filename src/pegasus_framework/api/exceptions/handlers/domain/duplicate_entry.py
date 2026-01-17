# pegasus_framework/api/exceptions/handlers/duplicate_entry.py
from fastapi import Request
from fastapi.responses import JSONResponse
from pegasus_framework.core.exceptions.domain.duplicate_entry import DuplicateEntityError
from pegasus_framework.api.v1.schemas.generic import ErrorResponse

async def duplicate_entity_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    
    assert isinstance(exc, DuplicateEntityError)

    payload = ErrorResponse(
        success=False,
        message=str(exc),
        error_code="DUPLICATE_ENTTITY",
        details=None,
    ).model_dump()


    return JSONResponse(
        status_code=409,
        content=payload,
    )