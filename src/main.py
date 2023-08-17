from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from redis import asyncio as aioredis
from src import redis
from src.config import app_configs, settings
from src.database import database
from src.stats.router import router as stats_router
from src.transactions.router import router as transactions_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    pool = aioredis.ConnectionPool.from_url(
        settings.REDIS_URL, max_connections=10, decode_responses=True
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)
    await database.connect()

    yield

    # Shutdown
    await database.disconnect()
    await redis.redis_client.close()


app = FastAPI(**app_configs)  # , lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


app.include_router(stats_router, tags=["Stats"])
app.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.on_event("startup")
async def startup() -> None:
    pool = aioredis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=10, decode_responses=True)
    redis.redis_client = aioredis.Redis(connection_pool=pool)
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
    if redis is not None and redis.redis_client is not None:
        await redis.redis_client.close()
