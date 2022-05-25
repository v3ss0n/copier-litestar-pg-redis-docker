import uuid
from typing import Any
from unittest.mock import MagicMock

import pytest
from starlite import TestClient

from app.main import app
from app.repositories.base import AbstractBaseRepository

from .utils import awaitable


@pytest.fixture
def patch_repo_delete(monkeypatch: Any) -> None:
    """
    Patched `AbstractBaseRepository._delete()` method that simply returns the instance
    passed to it.

    Include this fixture when testing `DELETE` routes.

    Parameters
    ----------
    monkeypatch : Any
    """

    def patch(_: Any, instance: Any) -> Any:
        return awaitable(instance)

    monkeypatch.setattr(AbstractBaseRepository, "_delete", patch)


@pytest.fixture
def patch_repo_add_flush_refresh(monkeypatch: Any) -> None:
    """
    Patched `AbstractBaseRepository._add_flush_refresh()` method.

    Inject this fixture when testing `POST`, `PUT` and `PATCH` endpoints.

    Parameters
    ----------
    monkeypatch : Any
    """

    def patch(_: Any, instance: Any) -> Any:
        if instance.id is None:
            instance.id = uuid.uuid4()
        return awaitable(instance)

    monkeypatch.setattr(AbstractBaseRepository, "_add_flush_refresh", patch)


@pytest.fixture
def patch_repo_scalar_404(monkeypatch: Any) -> None:
    """
    Patched `AbstractBaseRepository._scalar()` method.

    Inject this fixture when testing resource detail routes that should return 404.

    Parameters
    ----------
    monkeypatch : Any
    """
    monkeypatch.setattr(
        AbstractBaseRepository, "_scalar", MagicMock(return_value=awaitable(None))
    )


@pytest.fixture(scope="function")
def test_client() -> TestClient:

    return TestClient(app=app)
