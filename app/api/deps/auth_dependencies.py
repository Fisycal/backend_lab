# app/api/deps/auth_dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = AuthRepository(db)
    return AuthService(repo)