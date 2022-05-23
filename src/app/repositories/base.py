from abc import ABC
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from starlite.exceptions import NotFoundException

from app.db import AsyncScopedSession
from app.exceptions import RepositoryException
from app.models.base import Base, BaseModel
from app.utils.types import SupportsDict

DbType = TypeVar("DbType", bound=Base)
ReturnType = TypeVar("ReturnType", bound=BaseModel)


class AbstractBaseRepository(ABC, Generic[DbType, ReturnType]):
    """
    ABC for type Repository objects.

    Subclasses must set the `model` class variable.
    """

    db_model: type[DbType]
    return_model: type[ReturnType]

    def __init__(self) -> None:
        self.session = AsyncScopedSession()

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
        try:
            results = await self.session.execute(
                select(self.db_model).offset(offset).limit(limit)
            )
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
        return [self.return_model.from_orm(inst) for inst in results.scalars()]

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
        try:
            results = await self.session.execute(
                select(self.db_model).where(self.db_model.id == instance_id)
            )
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
        inst = results.scalar()
        if inst is None:
            raise NotFoundException
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
            instance = self.db_model(**data.dict())
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
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
        try:
            results = await self.session.execute(
                select(self.db_model).where(self.db_model.id == instance_id)
            )
            instance = results.scalar()
            if instance is None:
                raise NotFoundException
            for key, value in data.dict().items():
                setattr(instance, key, value)
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
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
        try:
            results = await self.session.execute(
                select(self.db_model).where(self.db_model.id == instance_id)
            )
            instance = results.scalar()
            if instance is None:
                raise NotFoundException
            await self.session.delete(instance)
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
        return self.return_model.from_orm(instance)
