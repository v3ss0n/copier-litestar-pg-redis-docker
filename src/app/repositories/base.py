from abc import ABC
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import RepositoryException
from app.models.base import Base
from app.utils import unstructure
from app.utils.types import DTOProtocol

T = TypeVar("T", bound=Base)


class AbstractBaseRepository(ABC, Generic[T]):
    model: type[T]

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_many(self, *, offset: int = 0, limit: int = 100) -> list[T]:
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(
                    select(self.model).offset(offset).limit(limit)
                )
                return list(results.scalars())
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def get_one(self, instance_id: UUID) -> T | None:
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(
                    select(self.model).where(self.model.id == instance_id)
                )
                return results.scalar()
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def create(self, data: DTOProtocol | dict[str, Any]) -> T:
        unstructured = unstructure(data)
        try:
            async with self.async_session as async_session:
                async with async_session.begin():
                    instance = self.model(**unstructured)
                    async_session.add(instance)
                    await async_session.flush()
                    await async_session.refresh(instance)
                    return instance
        except Exception as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def partial_update(self, instance_id: UUID, data: DTOProtocol) -> T:
        # TODO: what is the difference between this method and `get_one()`
        # TODO: such that type:ignore[no-any-return] is necessary here...?
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(
                    select(self.model).where(self.model.id == instance_id)
                )
                instance = results.scalar_one()
                for key, value in data.dict().items():
                    setattr(instance, key, value)
                async_session.add(instance)
                await async_session.flush()
                await async_session.refresh(instance)
                return instance  # type:ignore[no-any-return]
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def delete(self, instance_id: UUID) -> None:
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(
                    select(self.model).where(self.model.id == instance_id)
                )
                await async_session.delete(results)
                await async_session.commit()
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
