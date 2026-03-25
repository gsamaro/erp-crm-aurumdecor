from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings
from app.domain.base import Base
from app.domain.client import Client
from app.repositories.client_repository import ClientRepository
from app.security.crypto import encrypt_value


def test_client_repository_crud():
    settings.encryption_key = Fernet.generate_key().decode("utf-8")
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)

    with session_local() as db:
        repo = ClientRepository(db)
        client = Client(
            name="Cliente",
            phone=encrypt_value("111"),
            email=encrypt_value("cliente@example.com"),
        )

        created = repo.create(client)
        fetched = repo.get_by_id(created.id)

        assert created.id is not None
        assert fetched.email != "cliente@example.com"
