from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.routes import users, auth
from app.db.database import get_db
from app.config import settings

from fastapi.middleware.cors import CORSMiddleware

import logging

logging.basicConfig(
    level=logging.INFO,
    format=%(asctime)s | %(levelname)s |%(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
)

logger.info("Starting %s in %s mode", settings.APP_NAME, settings.ENVIRONMENT)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "message": f"{settings.APP_NAME} is running",
        "docs": "/docs",
        "health": "/health",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    logger.info("Health check endpoint accessed")
    db_status = "ok"

    try:
        db.execute(text("SELECT 1"))
        logger.info("Database health check passed")
    except Exception as e:
        db_status = "error"
        logger.info("Database health check failed: %s, e")

    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
        "database": db_status,
    }