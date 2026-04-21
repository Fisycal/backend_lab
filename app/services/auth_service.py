
from typing import Optional
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate_user(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def create_login_token(self, user):
        token_data = {
            "sub": user.email,
            "role": getattr(user, "role", "user"),
            "user_id": user.id,
        }
        return create_access_token(data=token_data)