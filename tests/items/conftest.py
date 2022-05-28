from typing import Any
from uuid import UUID, uuid4

import pytest

from app import api, models
from tests.utils import USER_ITEMS_PATH


@pytest.fixture
def user_id() -> UUID:
    return uuid4()


@pytest.fixture
def user(user_id: UUID) -> models.User:
    return models.User(
        id=user_id,
        username="Item Owner",
        is_active=True,
    )


@pytest.fixture
def unstructured_items(user_id: UUID) -> list[dict[str, Any]]:
    return [
        {"id": str(uuid4()), "name": "item 1", "owner_id": str(user_id)},
        {"id": str(uuid4()), "name": "item 2", "owner_id": str(user_id)},
    ]


@pytest.fixture
def unstructured_item(unstructured_items: list[dict[str, Any]]) -> dict[str, Any]:
    return unstructured_items[0]


@pytest.fixture
def db_items(unstructured_items: list[dict[str, Any]]) -> list[models.Item]:
    return [models.Item(**unstructured) for unstructured in unstructured_items]


@pytest.fixture
def db_item(db_items: list[models.Item]) -> models.Item:
    return db_items[0]


@pytest.fixture(autouse=True)
def patch_user_dependency(
    user: models.User, request: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Use indirect parametrization to provide a callable that is used for the patch,
    otherwise, patch returns `user`.

    E.g., `@pytest.mark.parametrize("patch_user_dependency", [NotFoundException], indirect=True)`
    """
    monkeypatch.setattr(
        api.items.item_router.dependencies["user"],  # type:ignore[index]
        "dependency",
        getattr(request, "param", lambda user_id, user_repository: user),
    )


@pytest.fixture
def user_items_path(user_id: UUID) -> str:
    return USER_ITEMS_PATH.format(user_id)


@pytest.fixture
def user_item_detail_path(db_item: models.Item, user_items_path: str) -> str:
    return f"{user_items_path}/{db_item.id}"
