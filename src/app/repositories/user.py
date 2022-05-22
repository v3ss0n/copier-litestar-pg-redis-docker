from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User
from app.utils import unstructure
from app.utils.security import get_password_hash, verify_password
from app.utils.types import DTOProtocol

from ..exceptions import RepositoryException
from .base import AbstractBaseRepository


class UserRepository(AbstractBaseRepository[User]):
    model = User

    async def create(self, data: DTOProtocol | dict[str, Any]) -> User | None:
        unstructured = unstructure(data)
        try:
            unstructured.update(
                hashed_password=get_password_hash(unstructured.pop("password"))
            )
            return await super().create(data=unstructured)
        except (TypeError, ValueError, AttributeError) as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def get_by_username(self, username: str) -> User | None:
        try:
            async with self.async_session as async_session:
                results = await async_session.execute(
                    select(User).where(User.username == username)
                )
                return cast(User | None, results.first())
        except SQLAlchemyError as e:
            raise RepositoryException("An exception occurred: " + repr(e)) from e

    async def authenticate(
        self, username: str, password: str
    ) -> User | None:  # todo remove hashed_pass
        user = await self.get_by_username(username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
