from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    SessionNotFoundError,
    InvalidSessionError,
    ForbiddenError,
    ValidationError,
)


def build_error(status_code: int, message: str, error_type: str = "http_error") -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "error": {
                "type": error_type,
                "message": message,
            },
        },
    )


def register_exception_handlers(app):

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(request: Request, exc: UserNotFoundError):
        return build_error(404, str(exc), "http_error")

    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
        return build_error(400, str(exc), "http_error")

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return build_error(401, str(exc), "http_error")

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(request: Request, exc: InvalidTokenError):
        return build_error(401, str(exc), "http_error")

    @app.exception_handler(SessionNotFoundError)
    async def session_missing_handler(request: Request, exc: SessionNotFoundError):
        return build_error(401, str(exc), "http_error")

    @app.exception_handler(InvalidSessionError)
    async def invalid_session_handler(request: Request, exc: InvalidSessionError):
        return build_error(401, str(exc), "http_error")

    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(request: Request, exc: ForbiddenError):
        return build_error(403, str(exc), "http_error")

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return build_error(400, str(exc), "http_error")

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError):
        return build_error(422, "Validation error", "validation_error")

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return build_error(exc.status_code, str(exc.detail), "http_error")