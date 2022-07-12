from dataclasses import dataclass
from uuid import UUID

from starlite import Dependency

from .types import BeforeAfter, CollectionFilter, LimitOffset


@dataclass
class Filters:
    id: CollectionFilter[UUID] | None
    created: BeforeAfter | None
    updated: BeforeAfter | None
    limit_offset: LimitOffset | None


def filters(
    id_filter: CollectionFilter[UUID] | None = Dependency(),
    created_filter: BeforeAfter | None = Dependency(),
    updated_filter: BeforeAfter | None = Dependency(),
    limit_offset: LimitOffset | None = Dependency(),
) -> Filters:
    """
    Aggregates filter dependencies to simplify injection.

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
