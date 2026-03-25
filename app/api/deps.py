from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    auth_service = AuthService(UserRepository(db))

    try:
        payload = auth_service.decode_access_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
