# fastapi
from fastapi import HTTPException, status, APIRouter
# fastapi response
from fastapi.responses import JSONResponse

# schemas
from routers.fuel_calculator.schemas import FuelParams

router = APIRouter()


@router.post("/routers/fuel_calculator/fuel/fuel_calculations")
async def fuel_calculations(payload: FuelParams):
    try:

        if not isinstance(payload.way, (int, float)) and isinstance(payload.fuel, (int, float)) and isinstance(
                payload.combustion, (int, float)) and isinstance(payload.remaining_values, (int, float)):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"detail": "Jedna z wartości nie jest liczbą!"})

        price = ((payload.combustion / 100) * payload.fuel * payload.way) + payload.remaining_values
        pattern = f"({payload.combustion} / 100) * {payload.fuel} * {payload.way} + {payload.remaining_values}"

        return {
            "price": str(price),
            "pattern": pattern
        }
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji obliecznia paliwa!")
