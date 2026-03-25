from app.domain.user import User
from app.services.user_service import UserService


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: list[User] = []

    def create(self, user: User) -> User:
        self.users.append(user)
        return user

    def get_by_id(self, user_id):
        return next((u for u in self.users if str(u.id) == str(user_id)), None)

    def list(self):
        return list(self.users)


class FakeAuthService:
    def __init__(self) -> None:
        self.last_password: str | None = None

    def hash_password(self, password: str) -> str:
        self.last_password = password
        return "hashed-" + password


def test_create_user_hashes_password():
    repo = FakeUserRepository()
    auth = FakeAuthService()
    service = UserService(repo, auth)

    user = service.create_user("Admin", "admin@example.com", "secret")

    assert user.password_hash == "hashed-secret"
    assert repo.users[0].email == "admin@example.com"
    assert auth.last_password == "secret"
