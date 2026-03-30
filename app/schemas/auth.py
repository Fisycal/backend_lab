from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User login email")
    password: str = Field(..., min_length=6, description="User password")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class MessageResponse(BaseModel):
    message: str

class UserPayload(BaseModel):
    user_id: int
    email: str
    role: str

class AuthUserResponse(BaseModel):
    message: str
    user: UserPayload