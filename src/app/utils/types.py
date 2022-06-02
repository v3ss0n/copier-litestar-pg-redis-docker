from datetime import datetime
from typing import Any, NamedTuple, Protocol


class SupportsDict(Protocol):
    """
    Protocol for typing parameters to any callable where the provided value must have a
    `dict()` method.
    """

    def dict(self) -> dict[str, Any]:
        """
        Method that returns an unstructured representation of self.

        Returns
        -------
        dict[str, Any]
        """


class BeforeAfter(NamedTuple):
    field_name: str
    before: datetime | None
    after: datetime | None


class LimitOffset(NamedTuple):
    limit: int | None
    offset: int | None
