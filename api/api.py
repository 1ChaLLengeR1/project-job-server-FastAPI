from fastapi import APIRouter

from api.auth.login import router as login_router
from api.patryk_router.one import router as patryk_router
from api.patryk_router.update import router as patryk_router_update

api_router = APIRouter()

api_router.include_router(login_router)
api_router.include_router(patryk_router)
api_router.include_router(patryk_router_update)
