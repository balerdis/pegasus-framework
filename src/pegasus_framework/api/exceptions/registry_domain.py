from fastapi import FastAPI
from pegasus_framework.core.exceptions.domain.duplicate_entry import DuplicateEntityError
from pegasus_framework.db.repositories.base_repository import EntityNotFoundError

from .handlers.domain.duplicate_entry import duplicate_entity_exception_handler
from .handlers.domain.entity_not_found import entity_not_found_handler


def register_domain_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        EntityNotFoundError,
        entity_not_found_handler,
    )

    app.add_exception_handler(
        DuplicateEntityError,
        duplicate_entity_exception_handler,
    )
