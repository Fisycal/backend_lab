from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.db.database import get_db
from app.db.models import User
from app.core.exceptions import AppException

from app.services.auth_service import AuthService
from app.api.deps.auth_dependencies import get_auth_service

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-jwt")
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service),
):
    return service.verify_token(credentials.credentials)


def require_authenticated_user(
    current_user=Depends(get_current_user),
):
    return current_user


def require_admin(
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return current_user

from fastapi import HTTPException, status


def require_owner_or_admin(
    current_user: dict,
    resource_user_id: int,
):
    is_admin = current_user.get("role") == "admin"
    is_owner = current_user.get("user_id") == resource_user_id

    if not is_admin and not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return True