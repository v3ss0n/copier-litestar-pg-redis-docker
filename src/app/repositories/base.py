import functools
from abc import ABC
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import Executable
from starlite.exceptions import NotFoundException

from app.db import AsyncScopedSession
from app.exceptions import RepositoryException
from app.models.base import Base, BaseModel
from app.utils.types import BeforeAfter, LimitOffset, SupportsDict

DbType = TypeVar("DbType", bound=Base)
ReturnType = TypeVar("ReturnType", bound=BaseModel)


def catch_sqlalchemy_exception(f: Any) -> Any:
    """
    Decorate a function or method to raise a `RepositoryException` chained from an
    original `SQLAlchemyError`.

        >>> import asyncio
        >>> @catch_sqlalchemy_exception
        ... async def db_error() -> None:
        ...     raise SQLAlchemyError("Original Exception")
        ...
        >>> try:
        ...     exc = asyncio.run(db_error())
        ... except RepositoryException as e:
        ...     print(f"caught repository exception from {type(e.__context__)}")
        ...
        caught repository exception from <class 'sqlalchemy.exc.SQLAlchemyError'>

    """

    @functools.wraps(f)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            return await f(*args, **kwargs)
        except SQLAlchemyError as e:
            raise RepositoryException(f"An exception occurred: {e}") from e

    return wrapped


class AbstractBaseRepository(ABC, Generic[DbType, ReturnType]):
    """
    ABC for resource type Repository objects.

    Subclasses must set the `db_model`, and `return_model` class variables.

    Class Attributes
    ----------------
    db_model : type[DbType]
        A SQLAlchemy declarative class.
    return_model : type[ReturnModel]
        Typed as a pydantic `BaseModel` class, but could really be anything with a
        `from_orm()` classmethod, that accepts an instance of `db_model` and returns
        something.
    """

    db_model: type[DbType]
    return_model: type[ReturnType]

    def __init__(self) -> None:
        self.session = AsyncScopedSession()
        self.base_select = select(self.db_model)

    @catch_sqlalchemy_exception
    async def _execute(self, statement: Executable, **kwargs: Any) -> Result:
        return await self.session.execute(statement, **kwargs)

    @catch_sqlalchemy_exception
    async def _add_flush_refresh(self, instance: DbType) -> DbType:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    @catch_sqlalchemy_exception
    async def _scalars(self, statement: Executable, **kwargs: Any) -> list[DbType]:
        result = await self._execute(statement, **kwargs)
        return list(result.scalars())

    @catch_sqlalchemy_exception
    async def _scalar(self, statement: Executable, **kwargs: Any) -> DbType:
        result = await self._execute(statement, **kwargs)
        instance = result.scalar()
        return instance  # type:ignore[no-any-return]

    @catch_sqlalchemy_exception
    async def _delete(self, instance: DbType) -> DbType:
        await self.session.delete(instance)
        await self.session.flush()
        return instance

    @staticmethod
    def _check_not_found(instance_or_none: DbType | None) -> DbType:
        if instance_or_none is None:
            raise NotFoundException
        return instance_or_none

    def apply_limit_offset_pagination(self, data: LimitOffset) -> None:
        """
        Paginate the base select query.

        Parameters
        ----------
        data : LimitOffset
        """
        self.base_select = self.base_select.limit(data.limit).offset(data.offset)

    def filter_on_datetime_field(self, data: BeforeAfter) -> None:
        """
        Add where-clause(s) to the query.

        Parameters
        ----------
        data : BeforeAfter
        """
        field = getattr(self.db_model, data.field_name)
        if data.before is not None:
            self.base_select = self.base_select.where(field < data.before)
        if data.after is not None:
            self.base_select = self.base_select.where(field > data.after)

    def _filter_select_by_kwargs(self, kwargs: dict[str, Any]) -> None:
        """
        Add where-clause(s) to the query.

        Parameters
        ----------
        kwargs : dict[str, Any]
            Keys must be names of attributes on ``self.db_model`` and values are tested
            on equality.
        """
        self.base_select = self.base_select.where(
            *(getattr(self.db_model, key) == value for key, value in kwargs.items())
        )

    async def get_many(self, **kwargs: Any) -> list[ReturnType]:
        """
        A list of `ReturnType` instances.

        Parameters
        ----------
        **kwargs : any
            each key/value pair added to where-clause of query as ``<key> == <value>``.

        Returns
        -------
        list[ReturnType]
        """
        self._filter_select_by_kwargs(kwargs)
        db_models = await self._scalars(self.base_select)
        return [self.return_model.from_orm(inst) for inst in db_models]

    async def get_one(self, instance_id: UUID) -> ReturnType:
        """
        A single `ReturnType` instance.

        Parameters
        ----------
        instance_id : UUID

        Returns
        -------
        ReturnType

        Raises
        ------
        NotFoundException
            If no instance found with `instance_id`.
        """
        inst = self._check_not_found(
            await self._scalar(self.base_select.where(self.db_model.id == instance_id))
        )
        return self.return_model.from_orm(inst)

    async def create(self, data: SupportsDict) -> ReturnType:
        """
        Create an instance of type `DbType` and return instance of `ReturnType` from it.

        Notes
        -----
            Does not support converting related items into SQLAlchemy instances. This
            could be done in the `data.dict()` method.

            If the model, `DbType` has relationship attributes without eager loading
            configured, attempting to access those attributes on the instance returned
            from this method will result in a SQLAlchemy `DetachedInstanceError`. See
            Preventing Implicit IO when Using AsyncSession_.

        Parameters
        ----------
        data : SupportsDict
            Anything that has a `dict()` method returning a mapping that is unpacked
            into `DbType` constructor.

        Returns
        -------
        ReturnType

        .. _See Preventing Implicit IO when Using AsyncSession:
            https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
        """
        instance = await self._add_flush_refresh(self.db_model(**data.dict()))
        return self.return_model.from_orm(instance)

    async def partial_update(self, instance_id: UUID, data: SupportsDict) -> ReturnType:
        """
        Update attributes on `DbType` retrieved with `instance_id` with keys and values
        found in mapping returned by `data.dict()`.

        Notes
        -----
            Does not support converting related items into SQLAlchemy instances. This
            could be done in the `data.dict()` method.

            If the model, `DbType` has relationship attributes without eager loading
            configured, attempting to access those attributes on the instance returned
            from this method will result in a SQLAlchemy `DetachedInstanceError`. See
            Preventing Implicit IO when Using AsyncSession_.

        Parameters
        ----------
        instance_id : UUID
        data : SupportsDict
            Anything that has a `dict()` method returning a mapping that is unpacked
            into `DbType` constructor.

        Returns
        -------
        ReturnType

        Raises
        ------
        NotFoundException

        .. _See Preventing Implicit IO when Using AsyncSession:
            https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
        """
        instance = self._check_not_found(
            await self._scalar(self.base_select.where(self.db_model.id == instance_id))
        )
        for key, value in data.dict().items():
            setattr(instance, key, value)
        instance = await self._add_flush_refresh(instance)
        return self.return_model.from_orm(instance)

    async def delete(self, instance_id: UUID) -> ReturnType:
        """
        Delete and return instance of type `DbType` represented by `instance_id`.

        Notes
        -----
            If the model, `DbType` has relationship attributes without eager loading
            configured, attempting to access those attributes on the instance returned
            from this method will result in a SQLAlchemy `DetachedInstanceError`. See
            Preventing Implicit IO when Using AsyncSession_.

        Parameters
        ----------
        instance_id : UUID

        Returns
        -------
        ReturnType

        Raises
        ------
        NotFoundException
        """
        instance = self._check_not_found(
            await self._scalar(self.base_select.where(self.db_model.id == instance_id))
        )
        await self._delete(instance)
        return self.return_model.from_orm(instance)
