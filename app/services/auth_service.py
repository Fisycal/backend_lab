import uuid
from app.repositories.auth_repository import AuthRepository
from app.utils.password import verify_password
from app.utils.jwt_handler import create_access_token, verify_access_token
from app.utils.session_store import sessions


class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def login_jwt(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        token = create_access_token({
            "sub": user.email,
            "role": user.role,
            "user_id": user.id
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def verify_jwt_user(self, token: str):
        return verify_access_token(token)

    def login_session(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

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

    def get_session_user(self, session_id: str):
        if not session_id:
            return "missing"

        session_data = sessions.get(session_id)

        if not session_data:
            return "invalid"

        return session_data

    def logout_session(self, session_id: str):
        if session_id and session_id in sessions:
            del sessions[session_id]

        return {"message": "Logged out from session"}

    def is_admin(self, payload: dict) -> bool:
        return payload.get("role") == "admin"