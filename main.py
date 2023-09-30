import uvicorn
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from auth.jwt_handler import check_access_token
from fastapi.middleware.cors import CORSMiddleware

#import routers
from auth import authentication
from routers.patryk_routers.calculator_work import calculator_earning
from routers.log_routers import log
from routers.list_products import list
from routers.outstanding_moeny import namesoverdue, outstandingmoney

app = FastAPI()
app.mount("/file", StaticFiles(directory="file"), name="file")

origins = [
    "https://arturscibor.pl",
    "https://arturscibor.pl/"
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#routers app
app.include_router(authentication.router)
app.include_router(calculator_earning.router)
app.include_router(log.router)
app.include_router(list.router)
app.include_router(namesoverdue.router)
app.include_router(outstandingmoney.router)

@app.get("/", dependencies=[Depends(check_access_token)])
def get():
    return "Przeszło!"