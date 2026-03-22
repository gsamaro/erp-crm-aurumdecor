from app.config.settings import settings
from app.domain.user import User
from app.services.auth_service import AuthService


class FakeUserRepository:
    def __init__(self, user: User | None = None) -> None:
        self.user = user

    def get_by_email(self, email: str):
        if self.user and self.user.email == email:
            return self.user
        return None


def test_hash_and_verify_password():
    service = AuthService(FakeUserRepository())
    hashed = service.hash_password("secret")

    assert service.verify_password("secret", hashed)
    assert not service.verify_password("wrong", hashed)


def test_authenticate_and_token_roundtrip():
    settings.secret_key = "test-secret"
    user = User(name="Admin", email="admin@example.com", password_hash="")
    service = AuthService(FakeUserRepository(user))

    hashed = service.hash_password("secret")
    user.password_hash = hashed

    authenticated = service.authenticate("admin@example.com", "secret")
    assert authenticated is user

    token = service.create_access_token("user-id")
    payload = service.decode_access_token(token)

    assert payload["sub"] == "user-id"
