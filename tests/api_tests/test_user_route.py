from http import HTTPStatus

from fintrack.domain.models.user import User


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
    client.post("/users", json=valid_create_user_request)
    call_arg = mock_user_repository.create.call_args[0][0]
    assert call_arg.username == valid_create_user_request["username"]
    assert call_arg.email == valid_create_user_request["email"]


def test_creating_user_returns_public_info(
    client, valid_create_user_request, mock_user_repository
):
    stored_user = User(
        id=123,
        username="stored username",
        email="stored@mail.com",
        hashed_password="stored_pass",
    )
    mock_user_repository.create.return_value = stored_user
    response = client.post("/users", json=valid_create_user_request)
    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json()
    assert response_data["id"] == stored_user.id
    assert response_data["username"] == stored_user.username
    assert response_data["email"] == stored_user.email
    assert "hashed_password" not in response_data
    assert "password" not in response_data


# TODO:
# Password is hashed before storing
# Data gets sanitized before storing
# Check for conflict on unique fields (username, email)
