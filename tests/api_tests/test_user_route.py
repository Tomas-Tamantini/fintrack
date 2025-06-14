from http import HTTPStatus


def test_posting_valid_user_returns_status_created(
    client, valid_create_user_request
):
    response = client.post("/users", json=valid_create_user_request)
    assert response.status_code == HTTPStatus.CREATED


def test_posting_user_with_invalid_email_returns_status_unprocessable_entity(
    client,
    invalid_email_create_user_request,
):
    response = client.post("/users", json=invalid_email_create_user_request)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_created_user_is_returned_without_password(
    client, valid_create_user_request
):
    response = client.post("/users", json=valid_create_user_request)
    assert "password" not in response.json()
