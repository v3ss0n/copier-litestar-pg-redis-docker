from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

ParamT = TypeVar("ParamT", bound=float | str | UUID)


@dataclass
class BeforeAfter:
    field_name: str
    before: datetime | None
    after: datetime | None


@dataclass
class CollectionFilter(Generic[ParamT]):
    field_name: str
    values: list[ParamT] | None


@dataclass
class LimitOffset:
    limit: int
    offset: int
