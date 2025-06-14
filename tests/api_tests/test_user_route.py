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


def test_created_user_has_correct_username_and_email(
    client, valid_create_user_request
):
    response = client.post("/users", json=valid_create_user_request)
    response_data = response.json()
    assert response_data["username"] == valid_create_user_request["username"]
    assert response_data["email"] == valid_create_user_request["email"]


def test_created_user_has_id(client, valid_create_user_request):
    response = client.post("/users", json=valid_create_user_request)
    response_data = response.json()
    assert "id" in response_data
    assert isinstance(response_data["id"], int)
