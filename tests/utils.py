from collections.abc import Coroutine
from typing import Any

from requests import Response


def awaitable(return_value: Any) -> Coroutine[Any, Any, Any]:
    async def coro() -> Any:
        return return_value

    return coro()


def check_response(response: Response, expected_status: int) -> None:
    if response.status_code != expected_status:
        print(str(response.text))
        raise RuntimeError(
            f"Response status code ({response.status_code}) does not equal expected "
            f"({expected_status})"
        )
