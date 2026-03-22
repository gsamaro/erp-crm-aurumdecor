from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientOut)
def create_client(
    payload: ClientCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = ClientRepository(db)
    service = ClientService(repo)
    return service.create_client(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        status=payload.status,
        notes=payload.notes,
    )


@router.get("", response_model=list[ClientOut])
def list_clients(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = ClientRepository(db)
    return repo.list()


@router.get("/{client_id}", response_model=ClientOut)
def get_client(
    client_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = ClientRepository(db)
    client = repo.get_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=ClientOut)
def update_client(
    client_id: str,
    payload: ClientUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = ClientRepository(db)
    client = repo.get_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    service = ClientService(repo)
    return service.update_client(client, payload.model_dump())
