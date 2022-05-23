from abc import ABC
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.db import AsyncScopedSession
from app.exceptions import RepositoryException
from app.models.base import Base
from app.utils import unstructure
from app.utils.types import DTOProtocol

T = TypeVar("T", bound=Base)


class AbstractBaseRepository(ABC, Generic[T]):
    model: type[T]

    def __init__(self) -> None:
        self.session = AsyncScopedSession()

    async def get_many(self, *, offset: int = 0, limit: int = 100) -> list[T]:
        try:
            results = await self.session.execute(
                select(self.model).offset(offset).limit(limit)
            )
            return list(results.scalars())
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def get_one(self, instance_id: UUID) -> T | None:
        try:
            results = await self.session.execute(
                select(self.model).where(self.model.id == instance_id)
            )
            return results.scalar()
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def create(self, data: DTOProtocol | dict[str, Any]) -> T:
        unstructured = unstructure(data)
        try:
            instance = self.model(**unstructured)
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
            return instance
        except Exception as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def partial_update(self, instance_id: UUID, data: DTOProtocol) -> T:
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
        try:
            results = await self.session.execute(
                select(self.model).where(self.model.id == instance_id)
            )
            await self.session.delete(results)
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
