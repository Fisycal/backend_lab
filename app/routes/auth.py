from fastapi import APIRouter, HTTPException, Response, Cookie, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.auth import LoginRequest, TokenResponse, MessageResponse
from app.services.auth_service import AuthService
from app.api.deps.auth_dependencies import get_auth_service


router = APIRouter()
security = HTTPBearer()


@router.post("/login-jwt", response_model=TokenResponse)
def login_jwt(
    credentials: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    result = service.login_jwt(credentials.email, credentials.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return result


@router.get("/me-jwt")
def get_me_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service)
):
    token = credentials.credentials
    payload = service.verify_jwt_user(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "message": "Authenticated with JWT",
        "user": payload
    }


@router.post("/login-session", response_model=MessageResponse)
def login_session(
    credentials: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service)
):
    result = service.login_session(credentials.email, credentials.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

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
    session_data = service.get_session_user(session_id)

    if session_data == "missing":
        raise HTTPException(status_code=401, detail="No session cookie found")

    if session_data == "invalid":
        raise HTTPException(status_code=401, detail="Invalid session")

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
    token = credentials.credentials
    payload = service.verify_jwt_user(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"message": "You are authenticated", "user": payload}


@router.get("/admin-jwt")
def admin_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service)
):
    token = credentials.credentials
    payload = service.verify_jwt_user(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not service.is_admin(payload):
        raise HTTPException(status_code=403, detail="Forbidden")

    return {
        "message": "Welcome Admin",
        "user": payload
    }