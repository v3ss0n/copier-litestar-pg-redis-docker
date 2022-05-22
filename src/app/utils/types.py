from typing import Any, Protocol


class DTOProtocol(Protocol):
    def dict(self) -> dict[str, Any]:
        ...
