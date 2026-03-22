from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(
    payload: UserCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    user_service = UserService(repo, auth_service)

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    if repo.get_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = user_service.create_user(payload.name, payload.email, payload.password)
    return user


@router.post("/bootstrap", response_model=UserOut)
def bootstrap(payload: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.count() > 0:
        raise HTTPException(status_code=400, detail="Bootstrap already completed")

    auth_service = AuthService(repo)
    user_service = UserService(repo, auth_service)
    user = user_service.create_user(payload.name, payload.email, payload.password)
    user.role = "admin"
    return repo.update(user)


@router.get("/bootstrap/status")
def bootstrap_status(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return {"allowed": repo.count() == 0}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    auth_service = AuthService(repo)

    user = auth_service.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth_service.create_access_token(str(user.id))
    return TokenResponse(access_token=token)
