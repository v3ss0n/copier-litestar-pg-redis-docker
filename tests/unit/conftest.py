from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock

import pytest
from litestar.contrib.repository.testing.generic_mock_repository import GenericMockRepository

from app import controllers
from app.domain import authors, countries
from app.lib import worker

if TYPE_CHECKING:
    from collections import abc


@pytest.fixture(scope="session", autouse=True)
def _patch_worker() -> "abc.Iterator":
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(worker.Worker, "on_app_startup", MagicMock())
    monkeypatch.setattr(worker.Worker, "stop", MagicMock())
    yield
    monkeypatch.undo()


@pytest.fixture(autouse=True)
def _author_repository(raw_authors: list[dict[str, Any]], monkeypatch: pytest.MonkeyPatch) -> None:
    repo_type = GenericMockRepository[authors.Author]
    repo_type.clear_collection()
    repo_type.seed_collection(authors.Author(**raw) for raw in raw_authors)
    monkeypatch.setattr(authors, "Repository", repo_type)
    monkeypatch.setattr(controllers.authors, "Repository", repo_type)


@pytest.fixture(autouse=True)
def _countries_repository(raw_countries: list[dict[str, Any]], monkeypatch: pytest.MonkeyPatch) -> None:
    repo_type = GenericMockRepository[countries.Country]
    repo_type.clear_collection()
    repo_type.seed_collection(countries.Country(**raw) for raw in raw_countries)
    monkeypatch.setattr(countries, "Repository", repo_type)
    monkeypatch.setattr(controllers.countries, "Repository", repo_type)
