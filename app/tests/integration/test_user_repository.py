from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.base import Base
from app.domain.user import User
from app.repositories.user_repository import UserRepository


def test_user_repository_crud():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)

    with session_local() as db:
        repo = UserRepository(db)
        user = User(name="Admin", email="admin@example.com", password_hash="hashed")

        created = repo.create(user)
        fetched = repo.get_by_email("admin@example.com")

        assert created.id is not None
        assert fetched.email == "admin@example.com"
