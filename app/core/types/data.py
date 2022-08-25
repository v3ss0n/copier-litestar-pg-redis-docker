from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Optional, TypeVar, Union

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID

ParamT = TypeVar("ParamT", bound=Union[float, str, "UUID"])


@dataclass
class BeforeAfter:
    field_name: str
    before: Optional["datetime"]
    after: Optional["datetime"]


@dataclass
class CollectionFilter(Generic[ParamT]):
    field_name: str
    values: list[ParamT] | None


@dataclass
class LimitOffset:
    limit: int
    offset: int
