from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None