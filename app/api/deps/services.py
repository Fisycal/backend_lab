from fastapi import Depends
from sqlalchemy.orm import Session
#from app.db.session import get_db
from app.db import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))