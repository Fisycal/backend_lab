from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserReplace, UserUpdate
from app.utils.password import hash_password
from app.core.exceptions import UserNotFoundError, UserAlreadyExistsError, ValidationError


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_users(self):
        return self.repo.get_all()

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        return user

    def create_user(self, user_data: UserCreate):
        existing_id = self.repo.get_by_id(user_data.id)
        if existing_id:
            raise UserAlreadyExistsError("User ID already exists")

        existing_email = self.repo.get_by_email(user_data.email)
        if existing_email:
            raise UserAlreadyExistsError("Email already exists")

        new_user = User(
            id=user_data.id,
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password),
            role=user_data.role
        )

        return self.repo.create(new_user)

    def replace_user(self, user_id: int, updated_user: UserReplace):
        if updated_user.id != user_id:
            raise ValidationError("Path user_id must match body id")

        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        email_owner = self.repo.get_by_email_excluding_user(updated_user.email, user_id)
        if email_owner:
            raise UserAlreadyExistsError("Email already exists")

        user.name = updated_user.name
        user.email = updated_user.email

        return self.repo.save(user)

    def update_user(self, user_id: int, updates: UserUpdate):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        update_data = updates.model_dump(exclude_unset=True)

        if "email" in update_data:
            email_owner = self.repo.get_by_email_excluding_user(update_data["email"], user_id)
            if email_owner:
                raise UserAlreadyExistsError("Email already exists")

        for field, value in update_data.items():
            setattr(user, field, value)

        return self.repo.save(user)

    def delete_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        self.repo.delete(user)
        return True

    def user_exists_for_head(self, user_id: int):
        user = self.repo.get_id_only(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        return user

    def any_users_exist(self):
        return self.repo.get_any_user_id()

    def user_exists_for_options(self, user_id: int):
        user = self.repo.get_id_only(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        return user