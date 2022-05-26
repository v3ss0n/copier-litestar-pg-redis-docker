import uuid
from typing import Any
from unittest.mock import MagicMock

from starlite import TestClient

from app.api import users
from app.models import UserReadModel

from .utils import USERS_PATH, awaitable, check_response


def test_cached_route(test_client: TestClient, monkeypatch: Any) -> None:
    id_ = uuid.uuid4()
    user = UserReadModel(username="testing", is_active=True, id=id_)
    get_one_mock = MagicMock(return_value=awaitable(user))
    monkeypatch.setattr(users.UserRepository, "get_one", get_one_mock)
    for _ in range(2):
        with test_client as client:
            response = client.get(f"{USERS_PATH}/{id_}")
        check_response(response, 200)
        assert response.json()["id"] == str(id_)
    get_one_mock.assert_called_once_with(instance_id=id_)
