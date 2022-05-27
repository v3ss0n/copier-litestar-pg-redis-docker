import uuid
from typing import Any

import pytest

from app import models
from tests.utils import USERS_PATH


@pytest.fixture
def unstructured_users() -> list[dict[str, Any]]:
    return [
        {
            "id": str(uuid.uuid4()),
            "username": "A User",
            "is_active": True,
            "password": "abc123",
        },
        {
            "id": str(uuid.uuid4()),
            "username": "B User",
            "is_active": False,
            "password": "123abc",
        },
    ]


@pytest.fixture
def unstructured_user(unstructured_users: list[dict[str, Any]]) -> dict[str, Any]:
    return unstructured_users[0]


@pytest.fixture
def db_users(
    unstructured_users: list[dict[str, Any]], monkeypatch: Any
) -> list[models.User]:
    # this speeds up the tests a little, the hashing takes about 0.2 secs/call
    monkeypatch.setattr(models.user, "get_password_hash", lambda s: s)
    return [
        models.User(**unstructured_user) for unstructured_user in unstructured_users
    ]


@pytest.fixture
def db_user(db_users: list[models.User]) -> models.User:
    return db_users[0]


@pytest.fixture
def users_path() -> str:
    return USERS_PATH


@pytest.fixture
def user_detail_path(db_user: models.User, users_path: str) -> str:
    return f"{users_path}/{db_user.id}"
