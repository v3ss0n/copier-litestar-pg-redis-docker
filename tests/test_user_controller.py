import uuid
from typing import Any
from unittest.mock import ANY, MagicMock

import pytest
from starlette import status
from starlite import TestClient

from app.constants import USER_CONTROLLER_PATH
from app.models.user import User
from app.repositories.user import UserRepository

from .utils import awaitable, check_response


@pytest.fixture
def unstructured_users() -> list[dict[str, Any]]:
    return [
        {
            "username": "A User",
            "is_active": True,
            "password": "abc123",
        },
        {
            "username": "B User",
            "is_active": False,
            "password": "123abc",
        },
    ]


@pytest.fixture
def unstructured_user(unstructured_users: list[dict[str, Any]]) -> dict[str, Any]:
    return unstructured_users[0]


@pytest.fixture
def db_users(unstructured_users: list[dict[str, Any]]) -> list[User]:
    return [
        User(id=uuid.uuid4(), **unstructured_user)
        for unstructured_user in unstructured_users
    ]


@pytest.fixture
def db_user(db_users: list[User]) -> User:
    return db_users[0]


@pytest.fixture
def patch_repo_scalars(db_users: list[User], monkeypatch: Any) -> None:
    """
    Patch the `AbstractBaseRepository._scalars()` method to return `db_users`.

    Parameters
    ----------
    db_users : list[User]
    monkeypatch : Any
    """
    monkeypatch.setattr(
        UserRepository, "_scalars", MagicMock(return_value=awaitable(db_users))
    )


@pytest.fixture
def patch_repo_scalar(db_user: User, monkeypatch: Any) -> None:
    """
    Patch the `AbstractBaseRepository._scalar()` method to return `db_user`.

    Parameters
    ----------
    db_user : User
    monkeypatch : Any
    """
    monkeypatch.setattr(
        UserRepository, "_scalar", MagicMock(return_value=awaitable(db_user))
    )


def test_create_user(
    unstructured_user: dict[str, str],
    test_client: TestClient,
    patch_repo_add_flush_refresh: None,
) -> None:
    with test_client as client:
        response = client.post("/v1" + USER_CONTROLLER_PATH, json=unstructured_user)
    check_response(response, status.HTTP_201_CREATED)
    assert response.json() == {
        "id": ANY,
        "username": "A User",
        "is_active": True,
    }


def test_create_user_invalid_payload(
    unstructured_user: dict[str, str], test_client: TestClient
) -> None:
    del unstructured_user["password"]
    with test_client as client:
        response = client.post("/v1" + USER_CONTROLLER_PATH, json=unstructured_user)
    check_response(response, status.HTTP_400_BAD_REQUEST)


def test_get_users(
    db_users: list[User], test_client: TestClient, patch_repo_scalars: None
) -> None:
    with test_client as client:
        response = client.get(f"/v1{USER_CONTROLLER_PATH}")
    check_response(response, status.HTTP_200_OK)
    db_ids = {str(user.id) for user in db_users}
    for user in response.json():
        assert user["id"] in db_ids


def test_get_user(
    db_user: User,
    unstructured_user: dict[str, Any],
    test_client: TestClient,
    patch_repo_scalar: None,
) -> None:
    with test_client as client:
        response = client.get(f"/v1{USER_CONTROLLER_PATH}/{db_user.id}")
    check_response(response, status.HTTP_200_OK)
    del unstructured_user["password"]
    assert response.json() == {**unstructured_user, **{"id": ANY}}


def test_get_user_404(test_client: TestClient, patch_repo_scalar_404: None) -> None:
    with test_client as client:
        response = client.get(f"/v1{USER_CONTROLLER_PATH}/{uuid.uuid4()}")
    check_response(response, status.HTTP_404_NOT_FOUND)


def test_put_user(
    db_user: User,
    unstructured_user: dict[str, Any],
    test_client: TestClient,
    patch_repo_add_flush_refresh: None,
    patch_repo_scalar: None,
) -> None:
    del unstructured_user["password"]
    unstructured_user["id"] = str(db_user.id)
    unstructured_user["username"] = "Morty"
    with test_client as client:
        response = client.put(
            f"/v1{USER_CONTROLLER_PATH}/{db_user.id}", json=unstructured_user
        )
    check_response(response, status.HTTP_200_OK)
    assert response.json() == unstructured_user


def test_put_user_404(
    unstructured_user: dict[str, Any],
    patch_repo_scalar_404: None,
    test_client: TestClient,
) -> None:
    random_id = str(uuid.uuid4())
    unstructured_user["id"] = random_id
    with test_client as client:
        response = client.put(
            f"/v1{USER_CONTROLLER_PATH}/{random_id}", json=unstructured_user
        )
    check_response(response, status.HTTP_404_NOT_FOUND)


def test_delete_user(
    db_user: User,
    unstructured_user: dict[str, Any],
    test_client: TestClient,
    patch_repo_delete: None,
    patch_repo_scalar: None,
) -> None:
    with test_client as client:
        response = client.delete(f"/v1{USER_CONTROLLER_PATH}/{db_user.id}")
    check_response(response, status.HTTP_200_OK)
    del unstructured_user["password"]
    assert response.json() == {**unstructured_user, **{"id": ANY}}


def test_delete_user_404(patch_repo_scalar_404: None, test_client: TestClient) -> None:
    with test_client as client:
        response = client.delete(f"/v1{USER_CONTROLLER_PATH}/{uuid.uuid4()}")
    check_response(response, status.HTTP_404_NOT_FOUND)
