import uuid
from typing import Any
from unittest.mock import ANY

import pytest
from starlette import status
from starlite import TestClient

from app.constants import USER_CONTROLLER_PATH

from .utils import check_response


@pytest.fixture
def unstructured_user() -> dict[str, Any]:
    return {
        "username": "Rick Sanchez",
        "is_active": True,
        "password": "wubbalubbadubdub",
    }


@pytest.fixture
def existing_user(
    unstructured_user: dict[str, Any], test_client: TestClient
) -> dict[str, Any]:
    with test_client as client:
        response = client.post("/v1" + USER_CONTROLLER_PATH, json=unstructured_user)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()  # type:ignore[no-any-return]


def test_create_user(
    unstructured_user: dict[str, str], test_client: TestClient
) -> None:
    with test_client as client:
        response = client.post("/v1" + USER_CONTROLLER_PATH, json=unstructured_user)
    check_response(response, status.HTTP_201_CREATED)
    assert response.json() == {
        "id": ANY,
        "username": "Rick Sanchez",
        "is_active": True,
    }


def test_create_user_invalid_payload(
    unstructured_user: dict[str, str], test_client: TestClient
) -> None:
    del unstructured_user["password"]
    with test_client as client:
        response = client.post("/v1" + USER_CONTROLLER_PATH, json=unstructured_user)
    check_response(response, status.HTTP_400_BAD_REQUEST)


def test_get_users(existing_user: dict[str, Any], test_client: TestClient) -> None:
    with test_client as client:
        response = client.get(f"/v1{USER_CONTROLLER_PATH}")
    check_response(response, status.HTTP_200_OK)
    for user in response.json():
        if user == existing_user:
            break
    else:
        raise RuntimeError("expected user not in response")


def test_get_user(existing_user: dict[str, Any], test_client: TestClient) -> None:
    with test_client as client:
        response = client.get(f"/v1{USER_CONTROLLER_PATH}/{existing_user['id']}")
    check_response(response, status.HTTP_200_OK)
    assert response.json() == existing_user


def test_get_user_404(test_client: TestClient) -> None:
    with test_client as client:
        response = client.get(f"/v1{USER_CONTROLLER_PATH}/{uuid.uuid4()}")
    check_response(response, status.HTTP_404_NOT_FOUND)


def test_put_user(existing_user: dict[str, Any], test_client: TestClient) -> None:
    existing_user["username"] = "Morty"
    with test_client as client:
        response = client.put(
            f"/v1{USER_CONTROLLER_PATH}/{existing_user['id']}", json=existing_user
        )
    check_response(response, status.HTTP_200_OK)
    assert response.json() == existing_user


def test_put_user_404(existing_user: dict[str, Any], test_client: TestClient) -> None:
    existing_user["username"] = "Morty"
    with test_client as client:
        response = client.put(
            f"/v1{USER_CONTROLLER_PATH}/{uuid.uuid4()}", json=existing_user
        )
    check_response(response, status.HTTP_404_NOT_FOUND)


def test_delete_user(existing_user: dict[str, Any], test_client: TestClient) -> None:
    with test_client as client:
        response = client.delete(f"/v1{USER_CONTROLLER_PATH}/{existing_user['id']}")
    check_response(response, status.HTTP_200_OK)
    assert response.json() == existing_user


def test_delete_user_404(test_client: TestClient) -> None:
    with test_client as client:
        response = client.delete(f"/v1{USER_CONTROLLER_PATH}/{uuid.uuid4()}")
    check_response(response, status.HTTP_404_NOT_FOUND)
