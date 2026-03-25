from app.domain.client import Client
from app.repositories.client_repository import ClientRepository
from app.security.crypto import decrypt_value, encrypt_value


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
            phone=encrypt_value(phone),
            email=encrypt_value(email),
            status=status,
            notes=encrypt_value(notes),
        )
        return self._decrypted_copy(self.client_repository.create(client))

    def update_client(self, client: Client, payload) -> Client:
        for field, value in payload.items():
            if value is not None:
                if field in {"phone", "email", "notes"}:
                    value = encrypt_value(value)
                setattr(client, field, value)
        return self._decrypted_copy(self.client_repository.update(client))

    def decrypt_client(self, client: Client) -> Client:
        return self._decrypted_copy(client)

    def _decrypted_copy(self, client: Client) -> Client:
        return Client(
            id=client.id,
            name=client.name,
            phone=decrypt_value(client.phone),
            email=decrypt_value(client.email),
            status=client.status,
            notes=decrypt_value(client.notes),
            created_at=client.created_at,
            updated_at=client.updated_at,
        )
