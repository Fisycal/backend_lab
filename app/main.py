from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.proxy_headers import ProxyHeadersMiddleware

from app.routes import users, auth
from app.db.database import get_db
from app.config import settings

from fastapi.middleware.cors import CORSMiddleware

import logging

import time
import uuid



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s |%(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


def validate_startup_settings() -> None:
    required_settings = {
        "DATABASE_URL": settings.DATABASE_URL,
        "SECRET_KEY": settings.SECRET_KEY,
        "APP_NAME": settings.APP_NAME,
        "APP_VERSION": settings.APP_VERSION,
        "ENVIRONMENT": settings.ENVIRONMENT,
    }

    missing_settings = [
        key for key, value in required_settings.items()
        if value is None or (isinstance(value, str) and not value.strip())
    ]

    if missing_settings:
        message = f"Missing required settings: {', '.join(missing_settings)}"
        logger.critical(message)
        raise RuntimeError(message)

    allowed_environments = {"development", "production", "test"}
    if settings.ENVIRONMENT not in allowed_environments:
        message = (
            f"Invalid ENVIRONMENT '{settings.ENVIRONMENT}'. "
            f"Expected one of: {', '.join(sorted(allowed_environments))}"
        )
        logger.critical(message)
        raise RuntimeError(message)

    logger.info("Startup settings validation passed")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
)

logger.info("Starting %s in %s mode", settings.APP_NAME, settings.ENVIRONMENT)
validate_startup_settings() # To quickly determine if startup and/or environment variables are missing

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS or ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(
        "REQUEST START | id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(
            "REQUEST ERROR | id=%s | error=%s",
            request_id,
            str(e)
        )
        raise

    process_time = (time.time() - start_time) * 1000

    logger.info(
        "REQUEST END | id=%s | status=%s | duration=%.2fms",
        request_id,
        response.status_code,
        process_time
    )

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"

    return response


app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "Validation error on %s %s: %s",
        request.method,
        request.url.path,
        exc.errors()
    )
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "error": {
                "type": "validation_error",
                "message": "request validation failed",
                "details": exc.errors()
            },
        },
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(
        "HTTP error on %s %s: %s",
        request.method,
        request.url.path,
        exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "type": "http_error",
                "message": exc.detail
            },
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled error on %s %s",
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": {
                "type": "internal_server_error",
                "message": "An unexpected error occurred",
            },
        },
    )




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