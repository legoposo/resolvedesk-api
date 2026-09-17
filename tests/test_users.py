import os


USER_EMAIL = os.getenv("TEST_USER_EMAIL")


def test_admin_can_list_users(client, admin_token):
    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_user_cannot_list_users(client, user_token):
    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403


def test_support_cannot_list_users(client, support_token):
    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {support_token}"
        },
    )

    assert response.status_code == 403


def test_user_can_access_self(client, user_token):
    response = client.get(
        "/users/2",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 200


def test_user_cannot_access_other_user(client, user_token):
    response = client.get(
        "/users/1",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403


def test_admin_can_access_any_user(client, admin_token):
    response = client.get(
        "/users/2",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200


def test_user_can_update_self(client, user_token):
    response = client.patch(
        "/users/2",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "name": "Maria Atualizada"
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Maria Atualizada"


def test_user_cannot_update_other_user(client, user_token):
    response = client.patch(
        "/users/1",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "name": "Tentativa Indevida"
        },
    )

    assert response.status_code == 403


def test_admin_can_update_any_user(client, admin_token):
    response = client.patch(
        "/users/4",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Severino Atualizado"
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Severino Atualizado"


def test_user_cannot_change_role(client, user_token):
    response = client.patch(
        "/users/2",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "role": "ADMIN"
        },
    )

    assert response.status_code == 403


def test_support_cannot_change_role(client, support_token):
    response = client.patch(
        "/users/4",
        headers={
            "Authorization": f"Bearer {support_token}"
        },
        json={
            "role": "ADMIN"
        },
    )

    assert response.status_code == 403


def test_admin_can_change_role(client, admin_token):
    response = client.patch(
        "/users/4",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "role": "USER"
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] == "USER"


def test_create_user_valid(client):
    response = client.post(
        "/users/",
        json={
            "name": "Carlos Teste",
            "email": "carlos@teste.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Carlos Teste"
    assert data["email"] == "carlos@teste.com"
    assert data["role"] == "USER"


def test_create_user_duplicate_email(client):
    response = client.post(
        "/users/",
        json={
            "name": "Outro Usuário",
            "email": USER_EMAIL,
            "password": "123456",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "E-mail já cadastrado"


def test_get_nonexistent_user(client, admin_token):
    response = client.get(
        "/users/9999",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"


def test_update_nonexistent_user(client, admin_token):
    response = client.patch(
        "/users/9999",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Usuário Fantasma"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"


def test_update_user_duplicate_email(client, admin_token):
    response = client.patch(
        "/users/4",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "email": USER_EMAIL
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "E-mail já cadastrado"


def test_user_can_update_email(client, user_token):
    response = client.patch(
        "/users/2",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "email": "maria.nova@teste.com"
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == "maria.nova@teste.com"


def test_user_can_update_password(client, admin_token):
    response = client.patch(
        "/users/2",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "password": "novaSenha123"
        },
    )

    assert response.status_code == 200


def test_admin_cannot_set_invalid_role(client, admin_token):
    response = client.patch(
        "/users/4",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "role": "SUPERMEGAADMIN"
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Perfil de usuário inválido"