from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.categories import router as categories_router
from app.api.tickets import router as tickets_router
from app.api.auth import router as auth_router


app = FastAPI(
    title="ResolveDesk API",
    description="API de Help Desk para gerenciamento de chamados.",
    version="0.1.0",
)

app.include_router(users_router)
app.include_router(categories_router)
app.include_router(tickets_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "name": "ResolveDesk API",
        "status": "online",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }