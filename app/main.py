from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.tickets import router as tickets_router
from app.api.categories import router as categories_router


tags_metadata = [
    {
        "name": "Auth",
        "description": (
            "Autenticação de usuários e consulta dos dados "
            "do usuário autenticado."
        ),
    },
    {
        "name": "Users",
        "description": (
            "Cadastro, consulta e gerenciamento de usuários "
            "e seus perfis de acesso."
        ),
    },
    {
        "name": "Tickets",
        "description": (
            "Criação, consulta, atualização, filtros "
            "e gerenciamento de chamados."
        ),
    },
    {
        "name": "Categories",
        "description": (
            "Gerenciamento das categorias utilizadas "
            "na classificação dos chamados."
        ),
    },
    {
        "name": "System",
        "description": (
            "Endpoints utilizados para verificar "
            "o funcionamento da API."
        ),
    },
]


app = FastAPI(
    title="ResolveDesk API",
    description=(
        "API REST de Help Desk desenvolvida com FastAPI e PostgreSQL. "
        "Possui autenticação JWT, controle de acesso por roles, "
        "gerenciamento de usuários, chamados e categorias."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tickets_router)
app.include_router(categories_router)


@app.get(
    "/",
    tags=["System"],
    summary="Informações da API",
    description="Retorna informações básicas e o status atual da ResolveDesk API.",
)
def root():
    return {
        "name": "ResolveDesk API",
        "status": "online",
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Verificar saúde da API",
    description=(
        "Endpoint utilizado para verificar rapidamente "
        "se a aplicação está respondendo."
    ),
)
def health_check():
    return {
        "status": "ok",
    }