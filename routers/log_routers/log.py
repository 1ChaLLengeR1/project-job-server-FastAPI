from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from routers.log_routers.schemas import Log
from database.Logs.models import Logs
from database.db import get_db
import datetime

router = APIRouter()


@router.post("/routers/log_routers/logs/add_log")
async def add_log(payload: Log, db: Session = Depends(get_db)):
    try:
        new_log = Logs(username=payload.username, description=payload.description, date=datetime.datetime.now())
        db.add(new_log)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Log został poprawnie dodany!"})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji dodawania dziennika!")


@router.get("/routers/log_routers/log/logs_values/{number}")
async def logs_values(number: int, db: Session = Depends(get_db)):
    try:

        if number == 0:
            item = db.query(Logs).order_by(Logs.date.desc()).all()
        else:
            item = db.query(Logs).order_by(Logs.date.desc()).limit(number).all()

        return item
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji wyświetlania logów!")
