from abc import ABC
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.db import AsyncScopedSession
from app.exceptions import RepositoryException
from app.models.base import Base
from app.utils import unstructure
from app.utils.types import SupportsDict

T = TypeVar("T", bound=Base)


class AbstractBaseRepository(ABC, Generic[T]):
    """
    ABC for type Repository objects.

    Subclasses must set the `model` class variable.
    """

    model: type[T]

    def __init__(self) -> None:
        self.session = AsyncScopedSession()

    async def get_many(self, *, offset: int = 0, limit: int = 100) -> list[T]:
        """
        Returns a list of `self.model` instances.

        Parameters
        ----------
        offset : int
        limit : int

        Returns
        -------
        list[T]
        """
        try:
            results = await self.session.execute(
                select(self.model).offset(offset).limit(limit)
            )
            return list(results.scalars())
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def get_one(self, instance_id: UUID) -> T | None:
        """
        Return a single instance of type `T`.

        Parameters
        ----------
        instance_id : UUID

        Returns
        -------
        T | None
        """
        try:
            results = await self.session.execute(
                select(self.model).where(self.model.id == instance_id)
            )
            return results.scalar()
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def create(self, data: SupportsDict | dict[str, Any]) -> T:
        """
        Create and instance of type `T` and return it.

        If the model, `T` has relationship attributes with out eager loading configured,
        attempting to access those attributes on the instance returned from this method
        will result in a SQLAlchemy `DetachedInstanceError`.

        Parameters
        ----------
        data : SupportsDict | dict[str, Any]

        Returns
        -------
        T
        """
        unstructured = unstructure(data)
        try:
            instance = self.model(**unstructured)
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
            return instance
        except Exception as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def partial_update(self, instance_id: UUID, data: SupportsDict) -> T:
        """
        Update attributes and values on `T` represented by `instance_id` with
        keys and values found in mapping returned by `data.dict()`.

        If the model, `T` has relationship attributes with out eager loading configured,
        attempting to access those attributes on the instance returned from this method
        will result in a SQLAlchemy `DetachedInstanceError`.

        Parameters
        ----------
        instance_id : UUID
        data : SupportsDict

        Returns
        -------
        T
        """
        try:
            results = await self.session.execute(
                select(self.model).where(self.model.id == instance_id)
            )
            instance: T = results.scalar_one()
            for key, value in data.dict().items():
                setattr(instance, key, value)
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def delete(self, instance_id: UUID) -> None:
        """
        Delete instance of type `T` represented by `instance_id`.

        Parameters
        ----------
        instance_id : UUID

        Returns
        -------
        None
        """
        try:
            results = await self.session.execute(
                select(self.model).where(self.model.id == instance_id)
            )
            await self.session.delete(results)
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
