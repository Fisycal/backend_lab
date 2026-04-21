from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.api.deps.services import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login-jwt", response_model=TokenResponse)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)):
    user = service.authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = service.create_login_token(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }