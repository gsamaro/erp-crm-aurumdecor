from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.base import Base
from app.domain.client import Client
from app.repositories.client_repository import ClientRepository


def test_client_repository_crud():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)

    with session_local() as db:
        repo = ClientRepository(db)
        client = Client(name="Cliente", phone="111", email="cliente@example.com")

        created = repo.create(client)
        fetched = repo.get_by_id(created.id)

        assert created.id is not None
        assert fetched.email == "cliente@example.com"
