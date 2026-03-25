from app.domain.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService) -> None:
        self.user_repository = user_repository
        self.auth_service = auth_service

    def create_user(self, name: str, email: str, password: str) -> User:
        password_hash = self.auth_service.hash_password(password)
        user = User(name=name, email=email, password_hash=password_hash)
        return self.user_repository.create(user)

    def get_user(self, user_id):
        return self.user_repository.get_by_id(user_id)

    def list_users(self):
        return self.user_repository.list()
