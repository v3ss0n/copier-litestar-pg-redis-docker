from datetime import datetime
from typing import Any
from unittest.mock import ANY, MagicMock

import pytest
from starlette import status
from starlite import TestClient

from app import models, repositories
from app.config import app_settings
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


@pytest.mark.parametrize(
    "params, call_kwargs",
    [
        ({}, {"before": None, "after": None}),
        (
            {"updated-before": str(datetime.max)},
            {"before": datetime.max, "after": None},
        ),
        ({"updated-after": str(datetime.min)}, {"before": None, "after": datetime.min}),
        (
            {"updated-before": str(datetime.max), "updated-after": str(datetime.min)},
            {"before": datetime.max, "after": datetime.min},
        ),
    ],
)
@pytest.mark.parametrize("patch_repo_scalars", ["db_users"], indirect=True)
def test_get_users_filter_by_updated(
    params: dict[str, str],
    call_kwargs: Any,
    users_path: str,
    test_client: TestClient,
    patch_repo_scalars: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _filter_select_by_updated_mock = MagicMock()
    monkeypatch.setattr(
        repositories.UserRepository,
        "_filter_select_by_updated",
        _filter_select_by_updated_mock,
    )
    with test_client as client:
        response = client.get(users_path, params=params)
    check_response(response, status.HTTP_200_OK)
    _filter_select_by_updated_mock.assert_called_once_with(**call_kwargs)


@pytest.mark.parametrize(
    "params, call_kwargs",
    [
        ({}, {"limit": app_settings.DEFAULT_PAGINATION_LIMIT, "offset": 0}),
        ({"page": 11}, {"limit": 100, "offset": 10}),
        ({"page-size": 11}, {"limit": 11, "offset": 0}),
        ({"page": 11, "page-size": 11}, {"limit": 11, "offset": 10}),
    ],
)
@pytest.mark.parametrize("patch_repo_scalars", ["db_users"], indirect=True)
def test_get_users_pagination(
    params: dict[str, str],
    call_kwargs: Any,
    users_path: str,
    test_client: TestClient,
    patch_repo_scalars: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _paginate_select_mock = MagicMock()
    monkeypatch.setattr(
        repositories.UserRepository,
        "_paginate_select",
        _paginate_select_mock,
    )
    with test_client as client:
        response = client.get(users_path, params=params)
    check_response(response, status.HTTP_200_OK)
    _paginate_select_mock.assert_called_once_with(**call_kwargs)


@pytest.mark.parametrize(
    "params, call_arg",
    [
        ({}, {"is_active": True}),
        ({"is-active": True}, {"is_active": True}),
        ({"is-active": False}, {"is_active": False}),
    ],
)
@pytest.mark.parametrize("patch_repo_scalars", ["db_users"], indirect=True)
def test_get_users_filter_by_is_active(
    params: dict[str, str],
    call_arg: Any,
    users_path: str,
    test_client: TestClient,
    patch_repo_scalars: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _filter_select_by_kwargs_mock = MagicMock()
    monkeypatch.setattr(
        repositories.UserRepository,
        "_filter_select_by_kwargs",
        _filter_select_by_kwargs_mock,
    )
    with test_client as client:
        response = client.get(users_path, params=params)
    check_response(response, status.HTTP_200_OK)
    _filter_select_by_kwargs_mock.assert_called_once_with(call_arg)


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
