from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock

import pytest
from starlite.contrib.repository.testing.generic_mock_repository import GenericMockRepository

from app.domain import authors
from app.lib import sqlalchemy_plugin, worker

if TYPE_CHECKING:
    from collections import abc
    from uuid import UUID


@pytest.fixture(scope="session", autouse=True)
def _patch_sqlalchemy_plugin() -> "abc.Iterator":
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        sqlalchemy_plugin.SQLAlchemyConfig,  # type:ignore[attr-defined]
        "on_shutdown",
        MagicMock(),
    )
    yield
    monkeypatch.undo()


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
    collection: dict["UUID", authors.Author] = {}
    for raw_author in raw_authors:
        author = authors.Author(**raw_author)
        collection[getattr(author, repo_type.id_attribute)] = author
    monkeypatch.setattr(repo_type, "collection", collection)
    monkeypatch.setattr(authors, "Repository", repo_type)
