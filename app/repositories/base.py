from abc import ABC
from typing import Any, Generic, TypeVar, cast
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import RepositoryException
from app.models.base import Base

T = TypeVar("T", bound=Base)


class AbstractBaseRepository(ABC, Generic[T]):
    model: type[T]

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_many(self, *, offset: int = 0, limit: int = 100) -> list[T]:
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(select(self.model).offset(offset).limit(limit))
                return cast(list[T], results.all())
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def get_one(self, instance_id: UUID) -> T | None:
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(select(self.model).where(self.model.id == instance_id))
                return cast(T | None, results.first())
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def create(self, data: BaseModel | dict[str, Any]) -> T | None:
        try:
            async with self.async_session as async_session:
                async with async_session.begin():
                    if isinstance(data, BaseModel):
                        data = data.dict()
                    instance = self.model(**data)
                    async_session.add(instance)
                    await async_session.commit()
                    await async_session.refresh(instance)
                    await async_session.dispose()
                    return cast(T, instance)
        except Exception as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def partial_update(self, instance_id: UUID, data: BaseModel) -> T:
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(select(self.model).where(self.model.id == instance_id))
                instance = results.first()
                for key, value in data.dict().items():
                    setattr(instance, key, value)
                async_session.add(instance)
                await async_session.commit()
                await async_session.refresh(instance)
                return cast(T, instance)
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def delete(self, instance_id: UUID) -> None:
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(select(self.model).where(self.model.id == instance_id))
                await async_session.delete(results)
                await async_session.commit()
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e
