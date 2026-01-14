# app/api/exceptions/register.py
from .handlers.duplicate_entry import duplicate_entity_exception_handler
from .handlers.entity_not_found import entity_not_found_handler
from .handlers.http_exception import http_exception_handler
from .handlers.unhandled import unhandled_exception_handler
from pegasus_framework.core.exceptions.domain.duplicate_entry import DuplicateEntityError
from pegasus_framework.db.repositories.base_repository import EntityNotFoundError   

from fastapi import FastAPI, HTTPException

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        EntityNotFoundError,
        entity_not_found_handler,
    )

    app.add_exception_handler(
        DuplicateEntityError,
        duplicate_entity_exception_handler,
    )

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )