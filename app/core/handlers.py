import itertools
from typing import TYPE_CHECKING

from starlite import Provide

from .filter_parameters import (
    created_filter,
    id_filter,
    limit_offset_pagination,
    updated_filter,
)
from .guards import CheckPayloadMismatch

if TYPE_CHECKING:
    from starlite.types import Guard


def create_pagination_dependencies() -> dict[str, Provide]:
    """
    Creates a dictionary of provides for pagination endpoints.
    Returns
    -------
    dict[str, Provide]

    """
    return {
        "limit_offset": Provide(limit_offset_pagination),
        "updated_filter": Provide(updated_filter),
        "created_filter": Provide(created_filter),
        "id_filter": Provide(id_filter),
    }


def resolve_id_guards(id_guard: str | tuple[str, str] | list[str | tuple[str, str]]) -> list["Guard"]:
    """Resolves guards by ID.

    Parameters
    ----------
    id_guard a guard id or collection of guard ids

    Returns
    -------
    resolved guards.
    """
    if isinstance(id_guard, str):
        return [CheckPayloadMismatch("id", id_guard).__call__]

    if isinstance(id_guard, tuple):
        return [CheckPayloadMismatch(*id_guard)]

    return list(itertools.chain.from_iterable(resolve_id_guards(t) for t in id_guard))
