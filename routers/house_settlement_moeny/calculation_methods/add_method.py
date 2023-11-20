from fastapi import Depends, status, HTTPException, APIRouter
# fastapi response
from fastapi.responses import JSONResponse
# schemas
from routers.house_settlement_moeny.calculation_methods.schemas import MainCounters

router = APIRouter()


@router.post('/routers/house_settlement_money/calculation_methods/add_method')
async def add_method(main_counters: MainCounters):
    try:
        return main_counters
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Błąd w skecji dodawania obliczeń mieszkań!")

# {
#     now_meter_electric:  15920,
#     now_meter_water:  275.850,
#     lately_meter_electric: 15286,
#     lately_meter_water: 262.277
# }
