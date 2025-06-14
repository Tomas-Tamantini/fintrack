from http import HTTPStatus


def test_creating_user_with_missing_fields_returns_unprocessable_entity(
    client,
):
    response = client.post("/users", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_user_with_invalid_email_returns_status_unprocessable_entity(
    client, invalid_email_create_user_request
):
    response = client.post("/users", json=invalid_email_create_user_request)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_user_returns_status_created(
    client, valid_create_user_request
):
    response = client.post("/users", json=valid_create_user_request)
    assert response.status_code == HTTPStatus.CREATED


def test_creating_user_delegates_persistence_to_repository(
    client, valid_create_user_request, mock_user_repository
):
    response = client.post("/users", json=valid_create_user_request)
    assert response.status_code == HTTPStatus.CREATED
    call_arg = mock_user_repository.create.call_args[0][0]
    assert call_arg.username == valid_create_user_request["username"]
    assert call_arg.email == valid_create_user_request["email"]


# TODO:
# Password is hashed before storing
# Data gets sanitized before storing
# Response contains only user ID, username, and email (no password)
# Check for conflict on unique fields (username, email)
