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
    client.post("/users", json=valid_create_user_request)
    call_arg = mock_user_repository.create.call_args[0][0]
    assert call_arg.username == valid_create_user_request["username"]
    assert call_arg.email == valid_create_user_request["email"]


def test_creating_user_sanitizes_input_before_storing(
    client, mock_user_repository
):
    dirty_request = {
        "username": "  User123  ",
        "email": "  a@b.com ",
        "password": "123",
    }
    client.post("/users", json=dirty_request)
    call_arg = mock_user_repository.create.call_args[0][0]
    assert call_arg.username == "User123"
    assert call_arg.email == "a@b.com"


def test_creating_user_returns_public_info(
    client, valid_create_user_request, mock_user_repository, user_stub
):
    mock_user_repository.create.return_value = user_stub
    response = client.post("/users", json=valid_create_user_request)
    response_data = response.json()
    assert response_data["id"] == user_stub.id
    assert response_data["username"] == user_stub.username
    assert response_data["email"] == user_stub.email
    assert "hashed_password" not in response_data
    assert "password" not in response_data


# TODO:
# Password is hashed before storing
# Ensure min/max name, email and password lengths are enforced
# Check for conflict on unique fields (username, email)
