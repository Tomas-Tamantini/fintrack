from http import HTTPStatus

from fintrack.api.authentication.jwt import TokenPair


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


def test_getting_token_with_correct_credentials_delegates_to_jwt_service(
    client,
    mock_user_repository,
    user_stub,
    mock_password_handler,
    mock_jwt_service,
):
    fake_tokens = {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
        "token_type": "Bearer",
    }
    mock_user_repository.get_by_email.return_value = user_stub
    mock_password_handler.verify.return_value = True
    mock_jwt_service.create_token_pair.return_value = TokenPair.model_validate(
        fake_tokens
    )
    response = client.post(
        "/auth/token",
        data={"username": "mail.exists.com", "password": "correct_password"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == fake_tokens
    mock_jwt_service.create_token_pair.assert_called_once_with(
        user_id=user_stub.email
    )
