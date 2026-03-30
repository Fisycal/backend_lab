import uuid
from fastapi import APIRouter, HTTPException, Header, Response, Cookie, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.utils.password import verify_password
from app.utils.jwt_handler import create_access_token, verify_access_token
from app.utils.session_store import sessions

from app.schemas.auth import LoginRequest, TokenResponse, MessageResponse


router = APIRouter()
security = HTTPBearer()

# JWT login route
@router.post("/login-jwt", response_model=TokenResponse)
def login_jwt(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "role": user.role,
        "user_id": user.id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Route for JWT
@router.get("/me-jwt")
def get_me_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "message": "Authenticated with JWT",
        "user": payload
    }


# Session login route
@router.post("/login-session", response_model=MessageResponse)
def login_session(credentials: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True
    )

    return {"message": "Logged in with session"}


# Route for session
@router.get("/me-session")
def get_me_session(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="No session cookie found")

    session_data = sessions.get(session_id)

    if not session_data:
        raise HTTPException(status_code=401, detail="Invalid session")

    return {
        "message": "Authenticated with session",
        "user": session_data
    }


# Logout session
@router.post("/logout-session", response_model=MessageResponse)
def logout_session(response: Response, session_id: str = Cookie(None)):
    if session_id and session_id in sessions:
        del sessions[session_id]

    response.delete_cookie("session_id")
    return {"message": "Logged out from session"}


# Protected route using JWT
@router.get("/protected-jwt")
def protected_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"message": "You are authenticated", "user": payload}


# Admin-only route using JWT
@router.get("/admin-jwt")
def admin_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    return {
        "message": "Welcome Admin",
        "user": payload
    }