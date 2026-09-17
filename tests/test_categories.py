import os

from fastapi.testclient import TestClient

from app.main import app


def test_authenticated_user_can_list_categories(client, user_token):
    response = client.get(
        "/categories/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_categories_without_token(client):
    response = client.get("/categories/")

    assert response.status_code == 401


def test_user_cannot_create_category(client, user_token):
    response = client.post(
        "/categories/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "name": "Software",
            "description": "Problemas de software",
        },
    )

    assert response.status_code == 403


def test_admin_can_create_category(client, admin_token):
    response = client.post(
        "/categories/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Software",
            "description": "Problemas de software",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Software"


def test_admin_cannot_create_duplicate_category(client, admin_token):
    response = client.post(
        "/categories/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Hardware",
            "description": "Categoria duplicada",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Categoria já cadastrada"