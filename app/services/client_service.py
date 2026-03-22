from app.domain.client import Client
from app.repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, client_repository: ClientRepository) -> None:
        self.client_repository = client_repository

    def create_client(
        self,
        name: str,
        phone: str | None,
        email: str | None,
        status: str,
        notes: str | None,
    ) -> Client:
        client = Client(
            name=name,
            phone=phone,
            email=email,
            status=status,
            notes=notes,
        )
        return self.client_repository.create(client)

    def update_client(self, client: Client, payload) -> Client:
        for field, value in payload.items():
            if value is not None:
                setattr(client, field, value)
        return self.client_repository.update(client)
