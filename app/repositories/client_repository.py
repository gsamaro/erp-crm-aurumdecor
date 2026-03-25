import uuid

from sqlalchemy.orm import Session

from app.domain.client import Client


class ClientRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def get_by_id(self, client_id):
        if isinstance(client_id, str):
            try:
                client_id = uuid.UUID(client_id)
            except ValueError:
                return None
        return self.db.query(Client).filter(Client.id == client_id).first()

    def list(self):
        return self.db.query(Client).order_by(Client.created_at.desc()).all()

    def update(self, client: Client) -> Client:
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client
