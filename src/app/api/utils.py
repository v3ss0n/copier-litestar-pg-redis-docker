from collections import abc
from datetime import datetime
from typing import Any

from starlite import BaseRouteHandler, NotAuthorizedException, Parameter, Request

from app.config import app_settings
from app.utils import BeforeAfter, LimitOffset

DTorNone = datetime | None


def filter_for_updated(
    before: DTorNone = Parameter(query="updated-before", default=None, required=False),
    after: DTorNone = Parameter(query="updated-after", default=None, required=False),
) -> BeforeAfter:
    """
    Return type consumed by `AbstractBaseRepository.filter_on_datetime_field()`.

    Parameters
    ----------
    before : datetime | None
        Filter for records updated before this date/time.
    after : datetime | None
        Filter for records updated after this date/time.
    """
    return BeforeAfter("updated_date", before, after)


def limit_offset_pagination(
    page: int = Parameter(ge=1, default=1, required=False),
    page_size: int = Parameter(
        query="page-size",
        ge=1,
        default=app_settings.DEFAULT_PAGINATION_LIMIT,
        required=False,
    ),
) -> LimitOffset:
    """
    Return type consumed by `AbstractBaseRepository.apply_limit_offset_pagination()`.

    Parameters
    ----------
    page : int
        LIMIT to apply to select.
    page_size : int
        OFFSET to apply to select.
    """
    return LimitOffset(page_size, page_size * (page - 1))


class CheckPayloadMismatch:
    def __init__(
        self,
        payload_key: str,
        path_key: str,
        compare_fn: abc.Callable[[Any, Any], bool] | None = None,
    ) -> None:
        """
        Create a callable class instance that can be used as a Guard function to check
        that path variables are equal to payload counterparts.

        Default behaviour is for the path variables to be coerced to a `str` before the
        comparison. This supports the common case of comparing a `str` identity from
        the payload to a UUID path parameter that has already been parsed into a UUID
        object.

        Parameters
        ----------
        payload_key : str
            Used to extract the value from the payload. If the key does not exist in
            the payload the value of the path parameter will be compared against `None`.
        path_key : str
            Name of the path parameter. This must be the name of a path parameter on
            the route to which the guard is applied, otherwise will raise `KeyError`.
        compare_fn : Callable[[Any, Any], bool] | None
            For custom comparison logic, pass a two parameter callable here that returns
            a `bool`.
        """
        self.payload_key = payload_key
        self.path_key = path_key
        if compare_fn is not None:
            self.compare_fn = staticmethod(compare_fn)
        else:
            self.compare_fn = self._compare

    @staticmethod
    def _compare(payload_value: Any, path_value: Any) -> bool:
        return payload_value == str(path_value)  # type:ignore[no-any-return]

    async def __call__(self, request: Request, _: BaseRouteHandler) -> None:
        """
        Ensure value of `self.payload_key` key in request payload matches the value of
        `self.path_key` in `Request.path_params`.

        By default, calls `str` on both values before comparing. For custom comparison
        provide a callable to `compare_fn` on instantiation.

        Parameters
        ----------
        request : Request
        _ : BaseRouteHandler

        Raises
        ------
        NotAuthorizedException
            If the value retrieved from the path does not test equal to the value
            retrieved from the request payload.
        """
        payload = await request.json() or {}
        payload_value = payload.get(self.payload_key)
        path_value = str(request.path_params[self.path_key])
        if not self.compare_fn(payload_value, path_value):
            raise NotAuthorizedException
