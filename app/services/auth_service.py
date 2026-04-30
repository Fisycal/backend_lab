import uuid
from app.repositories.auth_repository import AuthRepository
from app.utils.password import verify_password
from app.utils.jwt_handler import create_access_token, verify_access_token
from app.utils.session_store import sessions
from app.core.exceptions import InvalidCredentialsError, InvalidTokenError, SessionNotFoundError, InvalidSessionError,ForbiddenError


class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def login_jwt(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)

        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsError("Invalid credentials")

        token = create_access_token({
            "sub": user.email,
            "role": user.role,
            "user_id": user.id
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def verify_token(self, token: str):
        payload = verify_access_token(token)
        if not payload:
            raise InvalidTokenError("Invalid or expired token")
        return payload

    def login_session(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)

        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsError("Invalid credentials")

        session_id = str(uuid.uuid4())

        sessions[session_id] = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        }

        return {
            "session_id": session_id,
            "message": "Logged in with session"
        }

    def get_session_data(self, session_id: str):
        if not session_id:
            raise SessionNotFoundError("No session cookie found")

        session_data = sessions.get(session_id)
        if not session_data:
            raise InvalidSessionError("Invalid session")

        return session_data

    def logout_session(self, session_id: str):
        if session_id and session_id in sessions:
            del sessions[session_id]
        return {"message": "Logged out from session"}

    def require_admin(self, payload: dict):
        if payload.get("role") != "admin":
            raise ForbiddenError("Forbidden")
        return True