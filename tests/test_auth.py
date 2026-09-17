import os

from app.core.security import create_access_token


ADMIN_EMAIL = os.getenv("TEST_ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("TEST_ADMIN_PASSWORD")


def test_admin_list_tickets(client, admin_token):
    response = client.get(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_auth_me(client, admin_token):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["role"] == "ADMIN"


def test_login_invalid(client):
    response = client.post(
        "/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": "senha_errada123",
        },
    )

    assert response.status_code == 401


def test_tickets_without_token(client):
    response = client.get("/tickets/")

    assert response.status_code == 401


def test_login_valid(client):
    response = client.post(
        "/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_auth_me_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer token-invalido"
        },
    )

    assert response.status_code == 401


def test_auth_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_auth_me_with_nonexistent_user(client):
    token = create_access_token(subject="9999")

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 401