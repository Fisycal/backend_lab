from typing import Optional, Sequence
from sqlalchemy.orm import Session
from app.db.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_id_only(self, user_id: int):
        return self.db.query(User.id).filter(User.id == user_id).first()

    def get_any_user_id(self):
        return self.db.query(User.id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_by_email_excluding_user(self, email: str, user_id: int):
        return self.db.query(User).filter(User.email == email, User.id != user_id).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

    def save(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def commit(self) -> None:
        self.db.commit()

    def refresh(self, user: User) -> None:
        self.db.refresh(user)