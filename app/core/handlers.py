import itertools
from collections import abc
from typing import TYPE_CHECKING, Any

from pydantic import validate_arguments
from pydantic.typing import AnyCallable
from starlette.status import HTTP_200_OK
from starlite import BaseRouteHandler, Provide, Request
from starlite.enums import MediaType
from starlite.exceptions import HTTPException
from starlite.handlers import http as http_handlers
from starlite.response import Response
from starlite.types import (
    AfterRequestHandler,
    BeforeRequestHandler,
    CacheKeyBuilder,
    Guard,
    ResponseHeader,
)

from .filter_parameters import (
    created_filter,
    id_filter,
    limit_offset_pagination,
    updated_filter,
)
from .guards import CheckPayloadMismatch

__all__ = ["delete", "get", "get_collection", "patch", "post", "put"]

if TYPE_CHECKING:
    _B = http_handlers.HTTPRouteHandler
else:
    _B = object


class DescriptionMixin(_B):
    def __call__(self, fn: AnyCallable) -> _B:
        super().__call__(fn)
        if self.description is None and fn.__doc__ is not None:
            self.description = fn.__doc__
        return self


# noinspection PyPep8Naming
class get_collection(DescriptionMixin, http_handlers.get):
    @validate_arguments(config={"arbitrary_types_allowed": True})
    def __init__(  # pylint: disable=too-many-locals too-many-arguments
        self,
        path: str | list[str] | None = None,
        dependencies: dict[str, Provide] | None = None,
        guards: list[Guard] | None = None,
        opt: dict[str, Any] | None = None,
        after_request: AfterRequestHandler | None = None,
        before_request: BeforeRequestHandler | None = None,
        media_type: MediaType | str = MediaType.JSON,
        response_class: type[Response] | None = None,
        response_headers: dict[str, ResponseHeader] | None = None,
        status_code: int | None = None,
        cache: bool | int = False,
        cache_key_builder: CacheKeyBuilder | None = None,
        # OpenAPI related attributes
        content_encoding: str | None = None,
        content_media_type: str | None = None,
        deprecated: bool = False,
        description: str | None = None,
        include_in_schema: bool = True,
        operation_id: str | None = None,
        raises: list[type[HTTPException]] | None = None,
        response_description: str | None = None,
        summary: str | None = None,
        tags: list[str] | None = None,
        # sync only
        sync_to_thread: bool = False,
    ):
        """
        Wrapper around ``Starlite.get`` that adds standard collection route dependencies for
        filtering by created/updated timestamps, and limit/offset pagination.
        """
        dependencies = dependencies if dependencies is not None else {}
        default_dependencies: list[tuple[str, abc.Callable[..., Any]]] = [
            ("limit_offset", limit_offset_pagination),
            ("updated_filter", updated_filter),
            ("created_filter", created_filter),
            ("id_filter", id_filter),
        ]

        dependencies.update(
            {k: Provide(v) for k, v in default_dependencies if k not in dependencies}
        )
        super().__init__(
            path=path,
            dependencies=dependencies,
            guards=guards,
            opt=opt,
            after_request=after_request,
            before_request=before_request,
            media_type=media_type,
            response_class=response_class,
            response_headers=response_headers,
            status_code=status_code,
            cache=cache,
            cache_key_builder=cache_key_builder,
            content_encoding=content_encoding,
            content_media_type=content_media_type,
            deprecated=deprecated,
            description=description,
            include_in_schema=include_in_schema,
            operation_id=operation_id,
            raises=raises,
            response_description=response_description,
            summary=summary,
            tags=tags,
            sync_to_thread=sync_to_thread,
        )


def _resolve_id_guards(
    id_guard: str | tuple[str, str] | abc.Collection[str | tuple[str, str]]
) -> list[abc.Callable[[Request, BaseRouteHandler], abc.Awaitable[None]]]:
    if isinstance(id_guard, str):
        return [CheckPayloadMismatch("id", id_guard).__call__]

    if isinstance(id_guard, tuple):
        return [CheckPayloadMismatch(*id_guard)]

    return list(itertools.chain.from_iterable(_resolve_id_guards(t) for t in id_guard))


# noinspection PyPep8Naming
class put(DescriptionMixin, http_handlers.put):
    @validate_arguments(config={"arbitrary_types_allowed": True})
    def __init__(  # pylint: disable=too-many-locals too-many-arguments
        self,
        path: str | list[str] | None = None,
        dependencies: dict[str, Provide] | None = None,
        guards: list[Guard] | None = None,
        opt: dict[str, Any] | None = None,
        after_request: AfterRequestHandler | None = None,
        before_request: BeforeRequestHandler | None = None,
        media_type: MediaType | str = MediaType.JSON,
        response_class: type[Response] | None = None,
        response_headers: dict[str, ResponseHeader] | None = None,
        status_code: int | None = None,
        cache: bool | int = False,
        cache_key_builder: CacheKeyBuilder | None = None,
        # OpenAPI related attributes
        content_encoding: str | None = None,
        content_media_type: str | None = None,
        deprecated: bool = False,
        description: str | None = None,
        include_in_schema: bool = True,
        operation_id: str | None = None,
        raises: list[type[HTTPException]] | None = None,
        response_description: str | None = None,
        summary: str | None = None,
        tags: list[str] | None = None,
        # sync only
        sync_to_thread: bool = False,
        *,
        id_guard: str | tuple[str, str] | abc.Collection[str | tuple[str, str]] | None = None,
    ) -> None:
        """
        Wraps `Starlite.put`, adding the `id_guard` parameter.

        id_guard
        --------
        Can be a `str`, `tuple[str, str]`, or `abc.Collection[tuple[str, str]]`.
        - a single `str` should be the name of the path parameter that is checked against a body
        attribute called `"id"`.
        - a tuple, e.g., `("str_1", "str_2")` checks a payload attribute named `"str_1"` against
        a path parameter named `"str_2"`.
        - a collection of tuples, e.g., `[("str_1", "str_2")]` will perform checks identical to
        the tuple case, for each tuple in the collection.
        """
        if id_guard is not None:
            guards = guards or []
            guards.extend(_resolve_id_guards(id_guard))
        super().__init__(
            path=path,
            dependencies=dependencies,
            guards=guards,
            opt=opt,
            after_request=after_request,
            before_request=before_request,
            media_type=media_type,
            response_class=response_class,
            response_headers=response_headers,
            status_code=status_code,
            cache=cache,
            cache_key_builder=cache_key_builder,
            content_encoding=content_encoding,
            content_media_type=content_media_type,
            deprecated=deprecated,
            description=description,
            include_in_schema=include_in_schema,
            operation_id=operation_id,
            raises=raises,
            response_description=response_description,
            summary=summary,
            tags=tags,
            sync_to_thread=sync_to_thread,
        )


# noinspection PyPep8Naming
class patch(DescriptionMixin, http_handlers.put):
    @validate_arguments(config={"arbitrary_types_allowed": True})
    def __init__(  # pylint: disable=too-many-locals too-many-arguments
        self,
        path: str | list[str] | None = None,
        dependencies: dict[str, Provide] | None = None,
        guards: list[Guard] | None = None,
        opt: dict[str, Any] | None = None,
        after_request: AfterRequestHandler | None = None,
        before_request: BeforeRequestHandler | None = None,
        media_type: MediaType | str = MediaType.JSON,
        response_class: type[Response] | None = None,
        response_headers: dict[str, ResponseHeader] | None = None,
        status_code: int | None = None,
        cache: bool | int = False,
        cache_key_builder: CacheKeyBuilder | None = None,
        # OpenAPI related attributes
        content_encoding: str | None = None,
        content_media_type: str | None = None,
        deprecated: bool = False,
        description: str | None = None,
        include_in_schema: bool = True,
        operation_id: str | None = None,
        raises: list[type[HTTPException]] | None = None,
        response_description: str | None = None,
        summary: str | None = None,
        tags: list[str] | None = None,
        # sync only
        sync_to_thread: bool = False,
        *,
        id_guard: str | tuple[str, str] | abc.Collection[tuple[str, str]] | None = None,
    ) -> None:
        """
        Wraps `Starlite.patch`, adding the `id_guard` parameter.

        id_guard
        --------
        Can be a `str`, `tuple[str, str]`, or `abc.Collection[tuple[str, str]]`.
        - a single `str` should be the name of the path parameter that is checked against a body
        attribute called `"id"`.
        - a tuple, e.g., `("str_1", "str_2")` checks a payload attribute named `"str_1"` against
        a path parameter named `"str_2"`.
        - a collection of tuples, e.g., `[("str_1", "str_2")]` will perform checks identical to
        the tuple case, for each tuple in the collection.
        """
        if id_guard is not None:
            guards = guards or []
            guards.extend(_resolve_id_guards(id_guard))
        super().__init__(
            path=path,
            dependencies=dependencies,
            guards=guards,
            opt=opt,
            after_request=after_request,
            before_request=before_request,
            media_type=media_type,
            response_class=response_class,
            response_headers=response_headers,
            status_code=status_code,
            cache=cache,
            cache_key_builder=cache_key_builder,
            content_encoding=content_encoding,
            content_media_type=content_media_type,
            deprecated=deprecated,
            description=description,
            include_in_schema=include_in_schema,
            operation_id=operation_id,
            raises=raises,
            response_description=response_description,
            summary=summary,
            tags=tags,
            sync_to_thread=sync_to_thread,
        )


# noinspection PyPep8Naming
class delete(DescriptionMixin, http_handlers.delete):
    @validate_arguments(config={"arbitrary_types_allowed": True})
    def __init__(  # pylint: disable=too-many-locals too-many-arguments
        self,
        path: str | list[str] | None = None,
        dependencies: dict[str, Provide] | None = None,
        guards: list[Guard] | None = None,
        opt: dict[str, Any] | None = None,
        after_request: AfterRequestHandler | None = None,
        before_request: BeforeRequestHandler | None = None,
        media_type: MediaType | str = MediaType.JSON,
        response_class: type[Response] | None = None,
        response_headers: dict[str, ResponseHeader] | None = None,
        status_code: int | None = None,
        cache: bool | int = False,
        cache_key_builder: CacheKeyBuilder | None = None,
        # OpenAPI related attributes
        content_encoding: str | None = None,
        content_media_type: str | None = None,
        deprecated: bool = False,
        description: str | None = None,
        include_in_schema: bool = True,
        operation_id: str | None = None,
        raises: list[type[HTTPException]] | None = None,
        response_description: str | None = None,
        summary: str | None = None,
        tags: list[str] | None = None,
        # sync only
        sync_to_thread: bool = False,
    ) -> None:
        """
        Wraps ``Starlite.delete`` so we can override default status to 200.
        """
        super().__init__(
            path=path,
            dependencies=dependencies,
            guards=guards,
            opt=opt,
            after_request=after_request,
            before_request=before_request,
            media_type=media_type,
            response_class=response_class,
            response_headers=response_headers,
            status_code=status_code,
            cache=cache,
            cache_key_builder=cache_key_builder,
            content_encoding=content_encoding,
            content_media_type=content_media_type,
            deprecated=deprecated,
            description=description,
            include_in_schema=include_in_schema,
            operation_id=operation_id,
            raises=raises,
            response_description=response_description,
            summary=summary,
            tags=tags,
            sync_to_thread=sync_to_thread,
        )
        self.status_code = HTTP_200_OK


# noinspection PyPep8Naming
class get(DescriptionMixin, http_handlers.get):
    ...


# noinspection PyPep8Naming
class post(DescriptionMixin, http_handlers.post):
    ...
