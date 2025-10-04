from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from api.api import api_router

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from core.repository.psql.calendar.days.update import update_day_automatically_psql

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(update_day_automatically_psql, "cron", hour=0, minute=0)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(
    title="project_job",
    description="The project I use every day for my everyday work"
)

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


@app.get("/health")
async def health():
    return {"status": "ok"}
