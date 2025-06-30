from fastapi import FastAPI
from api.api import api_router

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="project_job",
              description="The project I use every day for my everyday work")

app.include_router(api_router)
Instrumentator().instrument(app).expose(app)
app.mount("/file", StaticFiles(directory="file"), name="file")

origins = [
    "https://arturscibor.pl",
    "https://praca.strona.arturscibor.pl",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "x-refresh-token", "UserData"],
    expose_headers=["Content-Disposition"],
)
