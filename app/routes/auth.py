from fastapi import APIRouter, Response, Cookie, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.auth import LoginRequest, TokenResponse, MessageResponse
from app.services.auth_service import AuthService
from app.api.deps.auth_dependencies import get_auth_service

from app.db.models import User 
from app.dependencies.auth import require_authenticated_user, require_admin

router = APIRouter(tags=["Auth"])
security = HTTPBearer()


@router.post("/login-jwt", response_model=TokenResponse)
def login_jwt(
    credentials: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    return service.login_jwt(credentials.email, credentials.password)


@router.get("/me-jwt")
def get_me_jwt(
    current_user: User = Depends(require_authenticated_user),
):
    return {
        "message": "Authenticated with JWT",
        "user": current_user,
    }


@router.post("/login-session", response_model=MessageResponse)
def login_session(
    credentials: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service)
):
    result = service.login_session(credentials.email, credentials.password)

    response.set_cookie(
        key="session_id",
        value=result["session_id"],
        httponly=True
    )

    return {"message": result["message"]}


@router.get("/me-session")
def get_me_session(
    session_id: str = Cookie(None),
    service: AuthService = Depends(get_auth_service)
):
    session_data = service.get_session_data(session_id)
    return {
        "message": "Authenticated with session",
        "user": session_data
    }


@router.post("/logout-session", response_model=MessageResponse)
def logout_session(
    response: Response,
    session_id: str = Cookie(None),
    service: AuthService = Depends(get_auth_service)
):
    result = service.logout_session(session_id)
    response.delete_cookie("session_id")
    return result


@router.get("/protected-jwt")
def protected_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service)
):
    payload = service.verify_token(credentials.credentials)
    return {"message": "You are authenticated", "user": payload}


@router.get("/admin-jwt")
def admin_jwt(
    current_user=Depends(require_admin),
):
    return {
        "message": "Welcome Admin",
        "user": current_user,
    }