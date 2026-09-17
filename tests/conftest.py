import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.core.security import hash_password
from app.models.user import User
from app.models.category import Category
from app.models.ticket import Ticket, TicketStatus
from sqlalchemy import create_engine, text
import pytest
from fastapi.testclient import TestClient
from app.main import app


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    response = client.post(
        "/auth/login",
        json={
            "email": os.getenv("TEST_ADMIN_EMAIL"),
            "password": os.getenv("TEST_ADMIN_PASSWORD"),
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def user_token(client):
    response = client.post(
        "/auth/login",
        json={
            "email": os.getenv("TEST_USER_EMAIL"),
            "password": os.getenv("TEST_USER_PASSWORD"),
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def support_token(client):
    response = client.post(
        "/auth/login",
        json={
            "email": os.getenv("TEST_SUPPORT_EMAIL"),
            "password": os.getenv("TEST_SUPPORT_PASSWORD"),
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]



TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db




def pytest_sessionstart(session):
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        admin = User(
            id=1,
            name="Leonardo Teste",
            email=os.getenv("TEST_ADMIN_EMAIL"),
            hashed_password=hash_password(
                os.getenv("TEST_ADMIN_PASSWORD")
            ),
            role="ADMIN",
        )

        user = User(
            id=2,
            name="Maria Teste",
            email=os.getenv("TEST_USER_EMAIL"),
            hashed_password=hash_password(
                os.getenv("TEST_USER_PASSWORD")
            ),
            role="USER",
        )

        support = User(
            id=4,
            name="Severino Teste",
            email=os.getenv("TEST_SUPPORT_EMAIL"),
            hashed_password=hash_password(
                os.getenv("TEST_SUPPORT_PASSWORD")
            ),
            role="SUPPORT",
        )

        category = Category(
            id=1,
            name="Hardware",
            description="Categoria de teste",
        )

        db.add_all([
            admin,
            user,
            support,
            category,
        ])

        db.commit()

        ticket_user = Ticket(
            id=1,
            title="Ticket da Maria",
            description="Ticket criado para teste de permissões",
            status=TicketStatus.OPEN.value,
            priority="MEDIUM",
            requester_id=2,
            category_id=1,
        )

        ticket_admin = Ticket(
            id=2,
            title="Ticket do Admin",
            description="Ticket criado para teste de permissões",
            status=TicketStatus.OPEN.value,
            priority="MEDIUM",
            requester_id=1,
            category_id=1,
        )

        db.add_all([
            ticket_user,
            ticket_admin,
        ])

        db.commit()


        db.execute(
            text(
                "SELECT setval(pg_get_serial_sequence('users', 'id'), "
                "(SELECT MAX(id) FROM users))"
            )
        )

        db.execute(
            text(
                "SELECT setval(pg_get_serial_sequence('categories', 'id'), "
                "(SELECT MAX(id) FROM categories))"
            )
        )

        db.execute(
            text(
                "SELECT setval(pg_get_serial_sequence('tickets', 'id'), "
                "(SELECT MAX(id) FROM tickets))"
            )
        )

        db.commit()   


    finally:
        db.close()


def pytest_sessionfinish(session, exitstatus):
    Base.metadata.drop_all(bind=engine)

    