# flake8: noqa
from typing import Any

from .security import get_password_hash
from .types import SupportsDict


def unstructure(data: SupportsDict | dict[str, Any]) -> dict[str, Any]:
    """
    Return an unstructured representation of `data`.

    If `data` is a dict, returns it untouched. Otherwise calls `.dict()` on `data`
    and returns the result.

    Parameters
    ----------
    data : SupportsDict | dict[str, Any]

    Returns
    -------
    dict[str, Any]
    """
    if isinstance(data, dict):
        return data
    return data.dict()
