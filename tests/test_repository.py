from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlite.testing import TestClient

from app.repositories.base import AbstractBaseRepository

from .utils import USERS_PATH, check_response


def test_sqlalchemy_error_wrapped(test_client: TestClient, monkeypatch: Any) -> None:
    monkeypatch.setattr(
        AbstractBaseRepository, "_execute", MagicMock(side_effect=SQLAlchemyError)
    )
    with test_client as client:
        response = client.get(f"{USERS_PATH}/{uuid4()}")
        check_response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
        assert "app.exceptions.RepositoryException" in response.text
