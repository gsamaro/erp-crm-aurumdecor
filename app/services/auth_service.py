from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from app.config.settings import settings
from app.domain.user import User
from app.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def _normalize_password(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) <= 72:
            return password
        return password_bytes[:72].decode("utf-8", errors="ignore")

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(self._normalize_password(password))

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(
            self._normalize_password(plain_password), hashed_password
        )

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.user_repository.get_by_email(email)
        if not user or not self.verify_password(password, user.password_hash):
            return None
        return user

    def create_access_token(self, subject: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_exp_minutes)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(
            payload, settings.secret_key, algorithm=settings.jwt_algorithm
        )

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
