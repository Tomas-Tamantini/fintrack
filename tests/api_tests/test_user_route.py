from http import HTTPStatus


def test_creating_user_with_missing_fields_returns_unprocessable_entity(
    client,
):
    response = client.post("/users", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    detail = response.json().get("detail", [])
    expected_num_missing_fields = 3
    assert expected_num_missing_fields == len(detail)


def test_creating_user_with_invalid_email_returns_status_unprocessable_entity(
    client, invalid_email_create_user_request
):
    response = client.post("/users", json=invalid_email_create_user_request)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    detail = response.json().get("detail", [])
    assert len(detail) == 1
    assert "not a valid email address" in detail[0]["msg"]


def test_creating_user_with_short_username_returns_status_unprocessable_entity(
    client, short_username_create_user_request
):
    response = client.post("/users", json=short_username_create_user_request)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    detail = response.json().get("detail", [])
    assert len(detail) == 1
    assert "at least 3 characters" in detail[0]["msg"]


def test_creating_user_with_long_username_returns_status_unprocessable_entity(
    client, long_username_create_user_request
):
    response = client.post("/users", json=long_username_create_user_request)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    detail = response.json().get("detail", [])
    assert len(detail) == 1
    assert "at most 50 characters" in detail[0]["msg"]


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
    client, mock_user_repository, valid_create_user_request
):
    dirty_request = valid_create_user_request
    dirty_request["username"] = "  User123  "
    dirty_request["email"] = "  \ta@b.com "
    client.post("/users", json=dirty_request)
    call_arg = mock_user_repository.create.call_args[0][0]
    assert call_arg.username == "User123"
    assert call_arg.email == "a@b.com"


def test_user_password_gets_hashed_before_being_stored(
    client,
    mock_user_repository,
    valid_create_user_request,
    mock_password_handler,
):
    req = valid_create_user_request
    req["password"] = "plain password"
    mock_password_handler.hash.return_value = "hashed"
    client.post("/users", json=req)
    assert mock_password_handler.hash.call_args[0][0] == "plain password"
    assert (
        mock_user_repository.create.call_args[0][0].hashed_password == "hashed"
    )


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
# Check for conflict on unique fields (username, email) on POST and PUT methods
# Get by ID returns public info
# Get by ID returns 404 if user not found
# Get by ID delegates to repository
# Delete by ID returns 204 if user deleted
# Delete by ID returns 404 if user not found
# Delete by ID delegates to repository
# Update by ID returns 200 if user updated
# Update by ID returns 404 if user not found
# Update by ID delegates to repository
# Update by ID returns 422 if request is invalid
# Update by ID checks for conflicts on unique fields (username, email)
# Get users returns status 200
# Get users returns list of public user info and total count
# Get users delegates to repository with pagination/filtering/sorting
