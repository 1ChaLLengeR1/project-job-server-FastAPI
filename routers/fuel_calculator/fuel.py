# fastapi
from fastapi import HTTPException, status, APIRouter

#chemas
from routers.fuel_calculator.schemas import FuelParams


router = APIRouter()


@router.post("/routers/fuel_calculator/fuel/fuel_calculations")
async def fuel_calculations(payload: FuelParams):
    try:

        price = ((payload.way/100) * payload.fuel * payload.combustion) + payload.remaining_values
        pattern = f"({payload.way} / 100) * {payload.fuel} * {payload.combustion} + {payload.remaining_values}"

        return {
            "price": str(price),
            "pattern": pattern
        }
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji obliecznia paliwa!")