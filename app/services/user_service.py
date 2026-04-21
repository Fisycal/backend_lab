from typing import Sequence, Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserReplace
from app.core.security import get_password_hash


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def list_users(self) -> Sequence[User]:
        return self.repo.get_all()

    def get_user(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def create_user(self, payload: UserCreate) -> User:
        existing_user = self.repo.get_by_email(payload.email)
        if existing_user:
            raise ValueError("Email already registered")

        new_user = User(
            email=payload.email,
            full_name=payload.full_name,
            is_active=payload.is_active if hasattr(payload, "is_active") else True,
            hashed_password=get_password_hash(payload.password),
        )
        return self.repo.create(new_user)

    def update_user_partial(self, user_id: int, payload: UserUpdate) -> Optional[User]:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing_user = self.repo.get_by_email(update_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        for field, value in update_data.items():
            if field == "password":
                setattr(user, "hashed_password", get_password_hash(value))
            else:
                setattr(user, field, value)

        self.repo.commit()
        self.repo.refresh(user)
        return user

    def replace_user(self, user_id: int, payload: UserReplace) -> Optional[User]:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None

        existing_user = self.repo.get_by_email(payload.email)
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already registered")

        user.email = payload.email
        user.full_name = payload.full_name
        user.is_active = payload.is_active
        user.hashed_password = get_password_hash(payload.password)

        self.repo.commit()
        self.repo.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.repo.get_by_id(user_id)
        if not user:
            return False

        self.repo.delete(user)
        return True