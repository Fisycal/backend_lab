from pydantic import BaseModel, EmailStr, Field

# Shared fields for user data.
class UserBase(BaseModel):
    name: str
    email: EmailStr

# Creating a new user.
class UserCreate(UserBase):
    id: int
    password: str = Field(..., min_length=6)
    role: str = "user"

# Full replacement with PUT
class UserReplace(UserBase):
    id: int

# For PATCH, where fields are optional
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

# For sending user data back to the client.
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

