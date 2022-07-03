from typing import Any
from unittest.mock import MagicMock

import pytest
import sqlalchemy as sa
from starlite import CacheConfig, Starlite, TestClient
from starlite.cache import SimpleCacheBackend

from app.main import app
from app.repositories.base import AbstractBaseRepository

from .utils import awaitable


@pytest.fixture
def patch_repo_delete(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Patched `AbstractBaseRepository._delete()` method that simply returns the instance
    passed to it.

    Include this fixture when testing `DELETE` routes.
    """

    def patch(_: Any, instance: Any) -> Any:
        return awaitable(instance)

    monkeypatch.setattr(AbstractBaseRepository, "_delete", patch)


@pytest.fixture
def patch_repo_add_flush_refresh(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Patched `_add_flush_refresh()` method.

    Inject this fixture when testing `POST`, `PUT` and `PATCH` endpoints.
    """

    def patch(_: Any, instance: Any) -> Any:
        """
        Returns the passed in instance.

        Patching out SQLAlchemy means that we don't get the default values populated
        on the object. This method looks for callable or constant default values
        provided for mapped attributes that haven't already been given a value and sets
        it on the model before returning.
        """
        instance_dict = vars(instance)
        mapper = sa.inspect(instance).mapper
        for column in mapper.columns:
            attr = mapper.get_property_by_column(column)
            if attr.key in instance_dict:
                continue
            if (default := getattr(column.default, "arg")) is not None:  # noqa: B009
                if callable(default):
                    setattr(instance, attr.key, default({}))
                else:
                    setattr(instance, attr.key, default)
        return awaitable(instance)

    monkeypatch.setattr(AbstractBaseRepository, "_add_flush_refresh", patch)


@pytest.fixture
def patch_repo_scalar_404(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Patched ``AbstractBaseRepository._scalar()`` method.

    Inject this fixture when testing resource detail routes that should return 404.
    """
    monkeypatch.setattr(
        AbstractBaseRepository, "_scalar", MagicMock(return_value=awaitable(None))
    )


@pytest.fixture
def patch_repo_scalar(request: Any, monkeypatch: Any) -> None:
    """
    Patch the ``AbstractBaseRepository._scalar()`` method.

    The model returned by the patch must be supplied via parametrization, e.g.::

        @pytest.mark.parametrize("patch_repo_scalar", ["db_model"], indirect=True)

    In the above example ``"db_model"`` is a fixture that provides the return value of
    the patch. The name of the fixture is passed as a string due to limitations within
    ``pytest``, see `here <https://github.com/pytest-dev/pytest/issues/349>`_ for more
    info.
    """
    monkeypatch.setattr(
        AbstractBaseRepository,
        "_scalar",
        MagicMock(return_value=awaitable(request.getfixturevalue(request.param))),
    )


@pytest.fixture
def patch_repo_scalars(request: Any, monkeypatch: Any) -> None:
    """
    Patch the ``AbstractBaseRepository._scalars()`` method to return ``db_users``.

    The models returned by the patch must be supplied via parametrization, e.g.::

        @pytest.mark.parametrize("patch_repo_scalars", ["db_models"], indirect=True)

    In the above example ``"db_models"`` is a fixture that provides the return value of
    the patch. The name of the fixture is passed as a string due to limitations within
    ``pytest``, see `here <https://github.com/pytest-dev/pytest/issues/349>`_ for more
    info.
    """
    monkeypatch.setattr(
        AbstractBaseRepository,
        "_scalars",
        MagicMock(return_value=awaitable(request.getfixturevalue(request.param))),
    )


@pytest.fixture
def starlite(monkeypatch: Any) -> Starlite:
    monkeypatch.setattr(app, "cache_config", CacheConfig(backend=SimpleCacheBackend()))
    return app


@pytest.fixture
def test_client(starlite: Starlite) -> TestClient:
    return TestClient(app=starlite)
