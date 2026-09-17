# ResolveDesk API

![Tests](https://github.com/legoposo/resolvedesk-api/actions/workflows/tests.yml/badge.svg)

API de Help Desk desenvolvida com FastAPI, PostgreSQL, JWT e controle de acesso por roles.

🚧 Projeto em desenvolvimento

## Tecnologias

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT
- PyJWT
- pwdlib
- Pydantic
- Pytest
- pytest-cov
- GitHub Actions

## Recursos

- Cadastro de usuários
- Autenticação com JWT
- Controle de acesso por roles
- Perfis USER, SUPPORT e ADMIN
- Criação de chamados
- Consulta de chamados
- Atualização de chamados
- Categorias de atendimento
- Filtros por status, prioridade e categoria
- Paginação
- Validação de dados
- Testes automatizados
- CI com GitHub Actions
- Banco separado para testes

## Perfis de acesso

### USER

- Criar chamados
- Visualizar os próprios chamados
- Atualizar os próprios dados
- Alterar e-mail e senha
- Não pode acessar chamados de outros usuários
- Não pode alterar roles

### SUPPORT

- Visualizar chamados
- Atualizar chamados
- Não pode administrar usuários
- Não pode alterar roles

### ADMIN

- Visualizar todos os chamados
- Atualizar qualquer chamado
- Listar usuários
- Consultar usuários
- Atualizar usuários
- Alterar roles
- Criar categorias

## Endpoints principais

### Autenticação

- `POST /auth/login`
- `GET /auth/me`

### Usuários

- `POST /users/`
- `GET /users/`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}`

### Chamados

- `POST /tickets/`
- `GET /tickets/`
- `GET /tickets/{ticket_id}`
- `PATCH /tickets/{ticket_id}`

### Categorias

- `GET /categories/`
- `POST /categories/`

## Filtros de chamados

O endpoint `GET /tickets/` aceita:

- `status_filter`
- `priority`
- `category_id`
- `skip`
- `limit`

Exemplo:

`GET /tickets/?status_filter=OPEN&priority=HIGH&category_id=1&skip=0&limit=20`

## Executando localmente

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/resolvedesk
SECRET_KEY=sua-chave-secreta
```

Execute as migrations:

```powershell
alembic upgrade head
```

Inicie a API:

```powershell
python -m uvicorn app.main:app --reload
```

A documentação Swagger ficará disponível em:

`http://127.0.0.1:8000/docs`

## Testes

O projeto possui testes automatizados com Pytest.

Execute:

```powershell
python -m pytest
```

A configuração atual exige cobertura mínima de **95%**.

A suíte cobre autenticação, autorização, usuários, chamados, categorias, filtros, paginação e validações.

## CI

O projeto utiliza GitHub Actions.

A cada `push` ou `pull request` na branch `main`, o GitHub executa automaticamente:

- Inicialização do PostgreSQL
- Instalação das dependências
- Execução do Pytest
- Verificação de cobertura

Se algum teste falhar ou a cobertura cair abaixo do mínimo configurado, o workflow falha.

## Estrutura do projeto

```text
resolvedesk-api/
├── .github/
│   └── workflows/
│       └── tests.yml
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── main.py
├── tests/
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── README.md
```

## Segurança

O projeto implementa:

- Autenticação com JWT
- Hash de senha
- Controle de acesso por roles
- Proteção de endpoints
- Validação de permissões
- Separação entre banco de desenvolvimento e banco de testes

## Status

🚧 Projeto em desenvolvimento
