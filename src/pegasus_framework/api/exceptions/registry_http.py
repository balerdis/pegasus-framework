from fastapi import FastAPI, HTTPException
from .handlers.http_exception import http_exception_handler
from .handlers.unhandled import unhandled_exception_handler


def register_http_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )
