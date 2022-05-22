# flake8: noqa
from typing import Any

from .security import get_password_hash, verify_password
from .types import DTOProtocol


def unstructure(data: DTOProtocol | dict[str, Any]) -> dict[str, Any]:
    if isinstance(data, dict):
        return data
    return data.dict()
