
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from config import APP_VERSION
from db import Database


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("app")

db = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting app version=%s", APP_VERSION)
    logger.info(
        "DB target: host=%s port=%s db=%s user=%s",
        db.host,
        db.port,
        db.name,
        db.user,
    )
    yield
    logger.info("Stopping app version=%s", APP_VERSION)


app = FastAPI(
    title="FastAPI Application Demo",
    version=APP_VERSION,
    lifespan=lifespan,
)


@app.get("/health", status_code=status.HTTP_200_OK)
def health() -> dict[str, str]:
    """Vérifie uniquement que l'API est en cours d'exécution"""
    return {
        "status": "ok",
        "service": "fastapi-app",
    }


@app.get("/version")
def version() -> dict[str, str]:
    """Retourne la version actuellement déployée"""
    return {"version": APP_VERSION}


@app.get("/ready")
def readiness() -> dict[str, str]:
    """Vérifie que l'API et sa base de données sont prêtes à servir du trafic"""
    try:
        db.ping()
        return {
            "status": "ready",
            "database": "ok",
        }
    except Exception as exc:
        logger.exception("Database readiness check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from exc