from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from api.api import api_router
from api.exception_handlers import register_exception_handlers
from config.rate_limit import limiter, rate_limit_exceeded_handler
from config.swagger_description.app import APP_DESCRIPTION
from config.swagger_description.summary import build_endpoint_summary
from config.swagger_description.tags import TAGS_METADATA
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
    description=build_endpoint_summary(api_router) + APP_DESCRIPTION,
    openapi_tags=TAGS_METADATA,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Rate limiting (slowapi)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS
origins = [
    "https://arturscibor.pl",
    "https://praca.strona.arturscibor.pl",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "x-refresh-token"],
)

# Globalne exception handlery (AppException + nieobsłużone wyjątki)
register_exception_handlers(app)

# Routery
app.include_router(api_router)

# Metryki Prometheus (/metrics)
Instrumentator().instrument(app).expose(app)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
