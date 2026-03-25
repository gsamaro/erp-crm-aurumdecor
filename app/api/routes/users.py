from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.get("", response_model=list[UserOut])
def list_users(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)
    return repo.list()
