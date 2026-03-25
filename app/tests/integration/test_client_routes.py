from cryptography.fernet import Fernet
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.settings import settings
from app.domain.base import Base
from app.main import app
from app.services.auth_service import AuthService
from app.domain.user import User


def setup_test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)
    return engine, session_local


def override_get_db(session_local):
    def _get_db():
        with session_local() as session:
            yield session

    return _get_db


def seed_admin(session_local):
    with session_local() as session:
        user = User(name="Admin", email="admin@example.com", password_hash="hashed")
        session.add(user)
        session.commit()
        session.refresh(user)
        token = AuthService(None).create_access_token(str(user.id))
        return token


def test_client_crud_routes():
    settings.secret_key = "test-secret-32-bytes-minimum-length"
    settings.encryption_key = Fernet.generate_key().decode("utf-8")
    engine, session_local = setup_test_db()

    from app.api.deps import get_db

    app.dependency_overrides[get_db] = override_get_db(session_local)

    token = seed_admin(session_local)
    client = TestClient(app)

    payload = {"name": "Cliente", "phone": "119999", "email": "cli@example.com"}
    created = client.post(
        "/clients",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert created.status_code == 200
    client_id = created.json()["id"]

    fetched = client.get(
        f"/clients/{client_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert fetched.status_code == 200
    assert fetched.json()["email"] == "cli@example.com"

    updated = client.put(
        f"/clients/{client_id}",
        json={"status": "inactive"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "inactive"

    listing = client.get("/clients", headers={"Authorization": f"Bearer {token}"})
    assert listing.status_code == 200
    assert len(listing.json()) == 1

    app.dependency_overrides.clear()
    engine.dispose()
