from .health import router as health_router
from .status import router as status_router
from .root import router as root_router

__all__ = [
    "health_router",
    "status_router",
    "root_router"
]