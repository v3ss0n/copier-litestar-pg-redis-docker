from typing import Any
from unittest.mock import ANY

import pytest
from starlette import status
from starlite import TestClient

from app import models
from tests.utils import USERS_PATH, check_response


@pytest.mark.parametrize("patch_repo_scalars", ["db_users"], indirect=True)
def test_get_users(
    db_users: list[models.User],
    users_path: str,
    test_client: TestClient,
    patch_repo_scalars: None,
) -> None:
    with test_client as client:
        response = client.get(users_path)
    check_response(response, status.HTTP_200_OK)
    db_ids = {str(user.id) for user in db_users}
    for user in response.json():
        assert user["id"] in db_ids


@pytest.mark.parametrize("patch_repo_scalar", ["db_user"], indirect=True)
def test_get_user(
    db_user: models.User,
    unstructured_user: dict[str, Any],
    test_client: TestClient,
    patch_repo_scalar: None,
) -> None:
    with test_client as client:
        response = client.get(f"{USERS_PATH}/{db_user.id}")
    check_response(response, status.HTTP_200_OK)
    del unstructured_user["password"]
    assert response.json() == unstructured_user


def test_post_user(
    unstructured_user: dict[str, str],
    users_path: str,
    test_client: TestClient,
    patch_repo_add_flush_refresh: None,
) -> None:
    del unstructured_user["id"]
    with test_client as client:
        response = client.post(users_path, json=unstructured_user)
    check_response(response, status.HTTP_201_CREATED)
    assert response.json() == {
        "id": ANY,
        "username": "A User",
        "is_active": True,
    }


def test_post_user_invalid_payload(
    unstructured_user: dict[str, str], users_path: str, test_client: TestClient
) -> None:
    del unstructured_user["password"]
    with test_client as client:
        response = client.post(users_path, json=unstructured_user)
    check_response(response, status.HTTP_400_BAD_REQUEST)


def test_get_user_404(
    user_detail_path: str, test_client: TestClient, patch_repo_scalar_404: None
) -> None:
    with test_client as client:
        response = client.get(user_detail_path)
    check_response(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.parametrize("patch_repo_scalar", ["db_user"], indirect=True)
def test_put_user(
    db_user: models.User,
    unstructured_user: dict[str, Any],
    user_detail_path: str,
    test_client: TestClient,
    patch_repo_add_flush_refresh: None,
    patch_repo_scalar: None,
) -> None:
    del unstructured_user["password"]
    unstructured_user["username"] = "Morty"
    with test_client as client:
        response = client.put(user_detail_path, json=unstructured_user)
    check_response(response, status.HTTP_200_OK)
    assert response.json() == unstructured_user


def test_put_user_404(
    unstructured_user: dict[str, Any],
    user_detail_path: str,
    patch_repo_scalar_404: None,
    test_client: TestClient,
) -> None:
    with test_client as client:
        response = client.put(user_detail_path, json=unstructured_user)
    check_response(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.parametrize("patch_repo_scalar", ["db_user"], indirect=True)
def test_delete_user(
    unstructured_user: dict[str, Any],
    user_detail_path: str,
    test_client: TestClient,
    patch_repo_delete: None,
    patch_repo_scalar: None,
) -> None:
    with test_client as client:
        response = client.delete(user_detail_path)
    check_response(response, status.HTTP_200_OK)
    del unstructured_user["password"]
    assert response.json() == unstructured_user


def test_delete_user_404(
    user_detail_path: str, test_client: TestClient, patch_repo_scalar_404: None
) -> None:
    with test_client as client:
        response = client.delete(user_detail_path)
    check_response(response, status.HTTP_404_NOT_FOUND)
