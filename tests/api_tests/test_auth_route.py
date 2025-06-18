from http import HTTPStatus


def test_getting_token_with_missing_fields_returns_unprocessable_entity(
    client,
):
    response = client.post("/auth/token", data={"bad": "data"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    detail = response.json().get("detail", [])
    expected_num_missing_fields = 2
    assert expected_num_missing_fields == len(detail)


def test_getting_token_with_inexistent_username_returns_unauthorized(
    client, mock_user_repository, mock_password_handler
):
    mock_user_repository.get_by_email.return_value = None
    mock_password_handler.verify.return_value = True
    response = client.post(
        "/auth/token",
        data={"username": "mail@not_exist.com", "password": "wrong_password"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json().get("detail") == "Incorrect email or password."


def test_getting_token_with_wrong_password_returns_unauthorized(
    client, mock_user_repository, user_stub, mock_password_handler
):
    mock_user_repository.get_by_email.return_value = user_stub
    mock_password_handler.verify.return_value = False
    response = client.post(
        "/auth/token",
        data={"username": "mail@exists.com", "password": "wrong_password"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json().get("detail") == "Incorrect email or password."
