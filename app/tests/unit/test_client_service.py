from app.domain.client import Client
from app.services.client_service import ClientService


class FakeClientRepository:
    def __init__(self) -> None:
        self.clients: list[Client] = []

    def create(self, client: Client) -> Client:
        self.clients.append(client)
        return client

    def update(self, client: Client) -> Client:
        return client


def test_create_client():
    repo = FakeClientRepository()
    service = ClientService(repo)

    client = service.create_client(
        name="Cliente",
        phone="119999",
        email="cli@example.com",
        status="active",
        notes=None,
    )

    assert client.email == "cli@example.com"
    assert repo.clients[0].name == "Cliente"


def test_update_client():
    repo = FakeClientRepository()
    service = ClientService(repo)
    client = Client(name="Cliente", phone="111", email="cli@example.com")

    updated = service.update_client(client, {"status": "inactive", "notes": "ok"})

    assert updated.status == "inactive"
    assert updated.notes == "ok"
