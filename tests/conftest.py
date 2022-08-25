from typing import TYPE_CHECKING, Any

import pytest
from starlite.cache import SimpleCacheBackend
from starlite.config import CacheConfig
from starlite.testing import TestClient

from app.main import app

if TYPE_CHECKING:
    from collections.abc import Generator

    from starlite import Starlite


@pytest.fixture()
def starlite(monkeypatch: Any) -> "Starlite":
    monkeypatch.setattr(app, "cache_config", CacheConfig(backend=SimpleCacheBackend()))
    return app


@pytest.fixture()
def test_client(starlite: "Starlite") -> "Generator[TestClient, None, None]":
    with TestClient(app=starlite) as client:
        yield client
