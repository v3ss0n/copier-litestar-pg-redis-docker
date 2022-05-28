from typing import Any
from unittest.mock import ANY, MagicMock
from uuid import UUID

import pytest
from starlette import status
from starlite import NotFoundException, TestClient

from app import models
from app.repositories import ItemRepository
from tests.utils import check_response, raise_exc


@pytest.mark.parametrize(
    "patch_user_dependency",
    [lambda user_id, user_repository: raise_exc(NotFoundException)],
    indirect=True,
)
def test_404_if_user_not_exists(
    user_items_path: str, test_client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_mock = MagicMock()
    monkeypatch.setattr(ItemRepository, "get_many_for_user", repo_mock)
    with test_client as client:
        response = client.get(user_items_path)
    check_response(response, status.HTTP_404_NOT_FOUND)
    repo_mock.assert_not_called()


@pytest.mark.parametrize("patch_repo_scalars", ["db_items"], indirect=True)
def test_get_items(
    user_id: UUID,
    db_items: list[models.Item],
    user_items_path: str,
    test_client: TestClient,
    patch_repo_scalars: None,
) -> None:
    with test_client as client:
        response = client.get(user_items_path)
    check_response(response, status.HTTP_200_OK)
    db_ids = {str(item.id) for item in db_items}
    for item in response.json():
        assert item["id"] in db_ids
        assert item["owner_id"] == str(user_id)


def test_post_item(
    unstructured_item: dict[str, Any],
    user_id: UUID,
    user_items_path: str,
    test_client: TestClient,
    patch_repo_add_flush_refresh: None,
) -> None:
    del unstructured_item["id"]
    del unstructured_item["owner_id"]
    with test_client as client:
        response = client.post(user_items_path, json=unstructured_item)
    check_response(response, status.HTTP_201_CREATED)
    assert response.json() == {
        "id": ANY,
        "name": unstructured_item["name"],
        "owner_id": str(user_id),
    }


@pytest.mark.parametrize("patch_repo_scalar", ["db_item"], indirect=True)
def test_get_item(
    db_item: models.Item,
    user_item_detail_path: str,
    test_client: TestClient,
    patch_repo_scalar: None,
) -> None:
    with test_client as client:
        response = client.get(user_item_detail_path)
        check_response(response, status.HTTP_200_OK)
        assert response.json() == {
            "id": str(db_item.id),
            "name": db_item.name,
            "owner_id": db_item.owner_id,
        }


def test_get_item_404(
    user_item_detail_path: str, test_client: TestClient, patch_repo_scalar_404: None
) -> None:
    with test_client as client:
        response = client.get(user_item_detail_path)
    check_response(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.parametrize("patch_repo_scalar", ["db_item"], indirect=True)
def test_put_item(
    unstructured_item: dict[str, Any],
    db_item: models.Item,
    user_item_detail_path: str,
    test_client: TestClient,
    patch_repo_scalar: None,
    patch_repo_add_flush_refresh: None,
) -> None:
    unstructured_item["name"] = "wowowowowowow"
    with test_client as client:
        response = client.put(user_item_detail_path, json=unstructured_item)
    check_response(response, status.HTTP_200_OK)
    assert response.json() == unstructured_item


def test_put_item_404(
    unstructured_item: dict[str, Any],
    user_item_detail_path: str,
    test_client: TestClient,
    patch_repo_scalar_404: None,
) -> None:
    with test_client as client:
        response = client.put(user_item_detail_path, json=unstructured_item)
    check_response(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.parametrize("patch_repo_scalar", ["db_item"], indirect=True)
def test_delete_item(
    unstructured_item: dict[str, Any],
    user_item_detail_path: str,
    test_client: TestClient,
    patch_repo_scalar: None,
    patch_repo_delete: None,
) -> None:
    with test_client as client:
        response = client.delete(user_item_detail_path)
    check_response(response, status.HTTP_200_OK)
    assert response.json() == unstructured_item


def test_delete_item_404(
    user_item_detail_path: str,
    test_client: TestClient,
    patch_repo_scalar_404: None,
) -> None:
    with test_client as client:
        response = client.delete(user_item_detail_path)
    check_response(response, status.HTTP_404_NOT_FOUND)
