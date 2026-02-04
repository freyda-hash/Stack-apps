
import os
import logging
from fastapi import FastAPI, HTTPException
from db import Database
from config import *

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("app")


app = FastAPI(title="FastAPI Application demo", version=APP_VERSION)

db = Database()

@app.on_event("startup")
def startup():
    logger.info("Starting app version=%s", APP_VERSION)
    logger.info("DB target: host=%s port=%s db=%s user=%s", db.host, db.port, db.name, db.user)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": APP_VERSION}

@app.get("/db/ping")
def db_ping():
    try:
        val = db.ping()
        return {"db": "ok", "result": val}
    except Exception as e:
        logger.exception("DB ping failed")
        raise HTTPException(status_code=503, detail=f"db unavailable: {type(e).__name__}")
