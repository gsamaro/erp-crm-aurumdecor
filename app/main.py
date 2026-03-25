from fastapi import Depends, FastAPI

from app.api.deps import get_current_user
from app.api.routes import auth, clients, users

app = FastAPI(title="ERP CRM Aurum Decor")


@app.get("/", dependencies=[Depends(get_current_user)])
def root():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(clients.router)
