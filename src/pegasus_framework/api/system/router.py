from fastapi import APIRouter
from pegasus_framework.api.system.health import router as health_router
from pegasus_framework.api.system.status import router as status_router
from pegasus_framework.api.system.root import router as root_router

router = APIRouter(tags=["SYSTEM"])

router.include_router(root_router)
router.include_router(health_router)
router.include_router(status_router)