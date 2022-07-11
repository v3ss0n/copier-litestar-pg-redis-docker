from collections.abc import Generator
from typing import Any

import pytest
from starlite import Starlite
from starlite.cache import SimpleCacheBackend
from starlite.config import CacheConfig
from starlite.testing import TestClient

from app.main import app


@pytest.fixture
def starlite(monkeypatch: Any) -> Starlite:
    monkeypatch.setattr(app, "cache_config", CacheConfig(backend=SimpleCacheBackend()))
    return app


@pytest.fixture
def test_client(starlite: Starlite) -> Generator[TestClient, None, None]:
    with TestClient(app=starlite) as client:
        yield client
