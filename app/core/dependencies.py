from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from starlite import Dependency

if TYPE_CHECKING:
    from uuid import UUID

    from .types import BeforeAfter, CollectionFilter, LimitOffset


@dataclass
class Filters:
    id: Optional["CollectionFilter[UUID]"]
    created: Optional["BeforeAfter"]
    updated: Optional["BeforeAfter"]
    limit_offset: Optional["LimitOffset"]


def filters(
    id_filter: Optional["CollectionFilter[UUID]"] = Dependency(),
    created_filter: Optional["BeforeAfter"] = Dependency(),
    updated_filter: Optional["BeforeAfter"] = Dependency(),
    limit_offset: Optional["LimitOffset"] = Dependency(),
) -> Filters:
    """Aggregates filter dependencies to simplify injection.

    Parameters
    ----------
    id_filter : CollectionFilter
    created_filter : BeforeAfter
    updated_filter : BeforeAfter
    limit_offset : LimitOffset

    Returns
    -------
    Filters
    """
    return Filters(
        id=id_filter,
        created=created_filter,
        updated=updated_filter,
        limit_offset=limit_offset,
    )
