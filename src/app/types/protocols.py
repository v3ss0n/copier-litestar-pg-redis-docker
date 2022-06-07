from typing import Any, Protocol


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
