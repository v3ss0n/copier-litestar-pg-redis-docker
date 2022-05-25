import uuid
from typing import Any
from unittest.mock import MagicMock

from sqlalchemy.exc import SQLAlchemyError
from starlite.testing import TestClient

from app.constants import USER_CONTROLLER_PATH
from app.repositories.base import AbstractBaseRepository

from .utils import check_response


def test_sqlalchemy_error_wrapped(test_client: TestClient, monkeypatch: Any) -> None:
    monkeypatch.setattr(
        AbstractBaseRepository, "_execute", MagicMock(side_effect=SQLAlchemyError)
    )
    with test_client as client:
        response = client.get(f"/v1{USER_CONTROLLER_PATH}/{uuid.uuid4()}")
        check_response(response, 500)
        assert "app.exceptions.RepositoryException" in response.text
