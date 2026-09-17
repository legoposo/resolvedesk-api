def test_user_cannot_access_other_ticket(client, user_token):
    response = client.get(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403


def test_support_can_access_any_ticket(client, support_token):
    response = client.get(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {support_token}"
        },
    )

    assert response.status_code == 200


def test_admin_can_access_any_ticket(client, admin_token):
    response = client.get(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200


def test_user_cannot_update_other_ticket(client, user_token):
    response = client.patch(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "status": "IN_PROGRESS"
        },
    )

    assert response.status_code == 403


def test_support_can_update_any_ticket(client, support_token):
    response = client.patch(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {support_token}"
        },
        json={
            "status": "IN_PROGRESS"
        },
    )

    assert response.status_code == 200


def test_admin_can_update_any_ticket(client, admin_token):
    response = client.patch(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "status": "RESOLVED"
        },
    )

    assert response.status_code == 200


def test_ticket_filter_by_status(client, admin_token):
    response = client.get(
        "/tickets/?status_filter=OPEN",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    for ticket in response.json():
        assert ticket["status"] == "OPEN"


def test_ticket_filter_by_priority(client, admin_token):
    response = client.get(
        "/tickets/?priority=MEDIUM",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    for ticket in response.json():
        assert ticket["priority"] == "MEDIUM"


def test_ticket_limit_validation(client, admin_token):
    response = client.get(
        "/tickets/?limit=101",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 422


def test_ticket_minimum_limit_validation(client, admin_token):
    response = client.get(
        "/tickets/?limit=0",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 422


def test_ticket_title_too_short(client, admin_token):
    response = client.post(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "Oi",
            "description": "Descrição válida para o teste",
            "category_id": 1,
            "priority": "MEDIUM",
        },
    )

    assert response.status_code == 422


def test_ticket_title_too_long(client, admin_token):
    response = client.post(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "A" * 121,
            "description": "Descrição válida para o teste",
            "category_id": 1,
            "priority": "MEDIUM",
        },
    )

    assert response.status_code == 422


def test_ticket_description_too_short(client, admin_token):
    response = client.post(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "Título válido",
            "description": "oi",
            "category_id": 1,
            "priority": "MEDIUM",
        },
    )

    assert response.status_code == 422


def test_ticket_description_too_long(client, admin_token):
    response = client.post(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "Título válido",
            "description": "A" * 2001,
            "category_id": 1,
            "priority": "MEDIUM",
        },
    )

    assert response.status_code == 422


def test_create_valid_ticket(client, admin_token):
    response = client.post(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "Impressora não funciona",
            "description": "A impressora não responde ao enviar documentos.",
            "category_id": 1,
            "priority": "HIGH",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Impressora não funciona"
    assert data["status"] == "OPEN"
    assert data["priority"] == "HIGH"
    assert data["requester_id"] == 1


def test_create_ticket_with_invalid_category(client, admin_token):
    response = client.post(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "Teste categoria inexistente",
            "description": "Este chamado usa uma categoria que não existe.",
            "category_id": 9999,
            "priority": "MEDIUM",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Categoria não encontrada"


def test_get_nonexistent_ticket(client, admin_token):
    response = client.get(
        "/tickets/9999",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chamado não encontrado"


def test_ticket_pagination(client, admin_token):
    response = client.get(
        "/tickets/?skip=0&limit=1",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_nonexistent_ticket(client, admin_token):
    response = client.patch(
        "/tickets/9999",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "status": "RESOLVED"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chamado não encontrado"


def test_update_ticket_with_invalid_category(client, admin_token):
    response = client.patch(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "category_id": 9999
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Categoria não encontrada"


def test_update_ticket_priority(client, admin_token):
    response = client.patch(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "priority": "URGENT"
        },
    )

    assert response.status_code == 200
    assert response.json()["priority"] == "URGENT"


def test_update_ticket_status(client, admin_token):
    response = client.patch(
        "/tickets/2",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "status": "IN_PROGRESS"
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"


def test_ticket_filter_by_category(client, admin_token):
    response = client.get(
        "/tickets/?category_id=1",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    for ticket in response.json():
        assert ticket["category_id"] == 1


def test_user_lists_only_own_tickets(client, user_token):
    response = client.get(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 200

    tickets = response.json()

    assert len(tickets) >= 1

    for ticket in tickets:
        assert ticket["requester_id"] == 2