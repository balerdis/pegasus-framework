# pegasus_framework/api/exceptions/registry_all.py
from fastapi import FastAPI

from .registry_domain import register_domain_exception_handlers
from .registry_auth import register_auth_exception_handlers
from .registry_http import register_http_exception_handlers


def register_all_exception_handlers(app: FastAPI) -> None:
    register_domain_exception_handlers(app)
    register_auth_exception_handlers(app)
    register_http_exception_handlers(app)
