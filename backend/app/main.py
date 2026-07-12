from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.calculations import router as calculations_router
from app.api.value_bets import router as value_bets_router
from app.api.predictions import router as predictions_router

app = FastAPI(
    title="AI Value Bet Finder API",
    description="Backend API for football statistics and value-bet analysis.",
    version="0.1.0",
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

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "AI Value Bet Finder API",
        "status": "running",
    }


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "version": "0.1.0",
    }