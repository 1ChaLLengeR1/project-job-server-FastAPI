from fastapi import APIRouter

from api.auth.login import router as login_router
from api.auth.login import router as automatically_login_router

api_router = APIRouter()

api_router.include_router(login_router)
api_router.include_router(automatically_login_router)
