from fastapi import APIRouter

from api.auth.login import router as login_router
from api.patryk_router.one import router as patryk_router
from api.patryk_router.update import router as patryk_router_update
from api.patryk_router.calculator import router as patryk_router_calculations
from api.outstanding_money.collection import router as collection_router_outstanding_money
from api.outstanding_money.create import router as create_router_outstanding_money
from api.outstanding_money.update import router as update_router_outstanding_money
from api.outstanding_money.delete import router as delete_router_outstanding_money


api_router = APIRouter()

api_router.include_router(login_router)
api_router.include_router(patryk_router)
api_router.include_router(patryk_router_update)
api_router.include_router(patryk_router_calculations)
api_router.include_router(collection_router_outstanding_money)
api_router.include_router(create_router_outstanding_money)
api_router.include_router(update_router_outstanding_money)
api_router.include_router(delete_router_outstanding_money)
