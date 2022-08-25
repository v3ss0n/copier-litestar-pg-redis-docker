from collections.abc import Coroutine, Sequence
from typing import Any, Generic

from requests import Response

from app.core import Repository
from app.core.repository.repository import T_base, T_model


class TestRepo(Repository[T_model], Generic[T_model]):
    many_response: list[T_model]
    one_response: T_model

    async def add_flush_refresh(self, instance: T_base) -> T_base:
        return instance

    async def get_many(self) -> Sequence[T_model]:
        return self.many_response

    async def get_one(self) -> T_model | None:
        return self.one_response

    async def create(self, data: dict[str, Any]) -> T_model:
        return self.model_type(**data)

    async def destroy(self) -> T_model:
        return self.one_response


def awaitable(return_value: Any) -> Coroutine[Any, Any, Any]:
    async def coro() -> Any:
        return return_value

    return coro()


def check_response(response: Response, expected_status: int) -> None:
    if response.status_code != expected_status:
        raise RuntimeError(f"Response status code ({response.status_code}) does not equal expected ({expected_status})")


def raise_exc(exc: type[Exception] | Exception) -> None:
    raise exc
