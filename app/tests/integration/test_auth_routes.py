from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.settings import settings
from app.domain.base import Base
from app.domain.user import User
from app.main import app
from app.services.auth_service import AuthService


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


def test_bootstrap_and_register_flow():
    settings.secret_key = "test-secret-32-bytes-minimum-length"
    engine, session_local = setup_test_db()

    from app.api.deps import get_db

    app.dependency_overrides[get_db] = override_get_db(session_local)

    client = TestClient(app)

    payload = {"name": "Admin", "email": "admin@example.com", "password": "secret"}
    response = client.post("/auth/bootstrap", json=payload)
    assert response.status_code == 200
    assert response.json()["role"] == "admin"

    response = client.post("/auth/bootstrap", json=payload)
    assert response.status_code == 400

    login = client.post("/auth/login", json={"email": "admin@example.com", "password": "secret"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.post(
        "/auth/register",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "User", "email": "user@example.com", "password": "secret"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"

    app.dependency_overrides.clear()
    engine.dispose()


def test_register_forbidden_for_non_admin():
    settings.secret_key = "test-secret-32-bytes-minimum-length"
    engine, session_local = setup_test_db()

    from app.api.deps import get_db

    app.dependency_overrides[get_db] = override_get_db(session_local)

    with session_local() as session:
        user = User(name="User", email="user@example.com", password_hash="hashed", role="user")
        session.add(user)
        session.commit()
        session.refresh(user)

        token = AuthService(None).create_access_token(str(user.id))

    client = TestClient(app)
    response = client.post(
        "/auth/register",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Blocked", "email": "blocked@example.com", "password": "secret"},
    )

    assert response.status_code == 403

    app.dependency_overrides.clear()
    engine.dispose()
