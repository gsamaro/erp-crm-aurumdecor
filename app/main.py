from fastapi import FastAPI

from app.api.routes import auth, clients, users

app = FastAPI(title="ERP CRM Aurum Decor")


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(clients.router)
