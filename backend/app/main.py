from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.automatic_fixture_value import (
    router as automatic_fixture_value_router,
)
from app.api.calculations import (
    router as calculations_router,
)
from app.api.database import (
    router as database_router,
)
from app.api.fixture_analysis import (
    router as fixture_analysis_router,
)
from app.api.fixture_value import (
    router as fixture_value_router,
)
from app.api.football import (
    router as football_router,
)
from app.api.market_evaluation import (
    router as market_evaluation_router,
)
from app.api.odds import (
    router as odds_router,
)
from app.api.predictions import (
    router as predictions_router,
)
from app.api.value_bets import (
    router as value_bets_router,
)

from app.database.session import (
    close_database,
    initialize_database,
)
from app.api.prediction_history import (
    router as prediction_history_router,
)

@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    await initialize_database()

    yield

    await close_database()


app = FastAPI(
    title="AI Value Bet Finder API",
    description=(
        "Backend API for football statistics, predictions, "
        "bookmaker odds and value-bet analysis."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["System"],
)
def root() -> dict[str, str]:
    return {
        "message": "AI Value Bet Finder API is running.",
    }


@app.get(
    "/health",
    tags=["System"],
)
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
    }


app.include_router(
    value_bets_router,
    prefix="/api",
)

app.include_router(
    calculations_router,
    prefix="/api",
)

app.include_router(
    predictions_router,
    prefix="/api",
)

app.include_router(
    football_router,
    prefix="/api",
)

app.include_router(
    fixture_analysis_router,
    prefix="/api",
)

app.include_router(
    market_evaluation_router,
    prefix="/api",
)

app.include_router(
    fixture_value_router,
    prefix="/api",
)

app.include_router(
    automatic_fixture_value_router,
    prefix="/api",
)

app.include_router(
    odds_router,
    prefix="/api",
)

app.include_router(
    database_router,
    prefix="/api",
)
app.include_router(
    prediction_history_router,
    prefix="/api",
)