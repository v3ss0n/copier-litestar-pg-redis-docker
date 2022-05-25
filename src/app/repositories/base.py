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
from app.utils.types import SupportsDict

DbType = TypeVar("DbType", bound=Base)
ReturnType = TypeVar("ReturnType", bound=BaseModel)


def wrap_sqla_exception(f: Any) -> Any:
    @functools.wraps(f)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            return await f(*args, **kwargs)
        except SQLAlchemyError as e:
            raise RepositoryException(f"An exception occurred: {e}") from e

    return wrapped


class AbstractBaseRepository(ABC, Generic[DbType, ReturnType]):
    """
    ABC for type Repository objects.

    Subclasses must set the `model` class variable.
    """

    db_model: type[DbType]
    return_model: type[ReturnType]

    def __init__(self) -> None:
        self.session = AsyncScopedSession()

    @wrap_sqla_exception
    async def _execute(self, statement: Executable, **kwargs: Any) -> Result:
        return await self.session.execute(statement, **kwargs)

    @wrap_sqla_exception
    async def _add_flush_refresh(self, instance: DbType) -> DbType:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    @wrap_sqla_exception
    async def _scalars(self, statement: Executable, **kwargs: Any) -> list[DbType]:
        result = await self._execute(statement, **kwargs)
        return list(result.scalars())

    @wrap_sqla_exception
    async def _scalar(self, statement: Executable, **kwargs: Any) -> DbType:
        result = await self._execute(statement, **kwargs)
        instance = result.scalar()
        return instance  # type:ignore[no-any-return]

    @wrap_sqla_exception
    async def _delete(self, instance: DbType) -> DbType:
        await self.session.delete(instance)
        await self.session.flush()
        return instance

    @staticmethod
    def _check_not_found(instance_or_none: DbType | None) -> DbType:
        if instance_or_none is None:
            raise NotFoundException
        return instance_or_none

    async def get_many(self, *, offset: int = 0, limit: int = 100) -> list[ReturnType]:
        """
        Returns a list of `self.model` instances.

        Parameters
        ----------
        offset : int
        limit : int

        Returns
        -------
        list[ReturnType]
        """
        db_models = await self._scalars(
            select(self.db_model).offset(offset).limit(limit)
        )
        return [self.return_model.from_orm(inst) for inst in db_models]

    async def get_one(self, instance_id: UUID) -> ReturnType:
        """
        Return a single instance of type `DbType`.

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
        inst = self._check_not_found(
            await self._scalar(
                select(self.db_model).where(self.db_model.id == instance_id)
            )
        )
        return self.return_model.from_orm(inst)

    async def create(self, data: SupportsDict) -> ReturnType:
        """
        Create and instance of type `DbType` and return it.

        If the model, `DbType` has relationship attributes without eager loading
        configured, attempting to access those attributes on the instance returned from
        this method will result in a SQLAlchemy `DetachedInstanceError`.

        Parameters
        ----------
        data : SupportsDict | dict[str, Any]

        Returns
        -------
        ReturnType
        """
        try:
            instance = await self._add_flush_refresh(self.db_model(**data.dict()))
        except Exception as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
        return self.return_model.from_orm(instance)

    async def partial_update(self, instance_id: UUID, data: SupportsDict) -> ReturnType:
        """
        Update attributes and values on `DbType` represented by `instance_id` with
        keys and values found in mapping returned by `data.dict()`.

        If the model, `DbType` has relationship attributes without eager loading
        configured, attempting to access those attributes on the instance returned from
        this method will result in a SQLAlchemy `DetachedInstanceError`.

        Parameters
        ----------
        instance_id : UUID
        data : SupportsDict

        Returns
        -------
        ReturnType

        Raises
        ------
        NotFoundException
        """
        instance = self._check_not_found(
            await self._scalar(
                select(self.db_model).where(self.db_model.id == instance_id)
            )
        )
        for key, value in data.dict().items():
            setattr(instance, key, value)
        instance = await self._add_flush_refresh(instance)
        return self.return_model.from_orm(instance)

    async def delete(self, instance_id: UUID) -> ReturnType:
        """
        Delete instance of type `DbType` represented by `instance_id`.

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
            await self._scalar(
                select(self.db_model).where(self.db_model.id == instance_id)
            )
        )
        await self._delete(instance)
        return self.return_model.from_orm(instance)
