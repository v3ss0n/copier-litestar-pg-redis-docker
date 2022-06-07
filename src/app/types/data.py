from datetime import datetime
from typing import NamedTuple


class BeforeAfter(NamedTuple):
    field_name: str
    before: datetime | None
    after: datetime | None


class LimitOffset(NamedTuple):
    limit: int
    offset: int
