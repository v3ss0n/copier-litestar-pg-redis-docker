from typing import Any

from app.models.user import User
from app.utils import unstructure
from app.utils.security import get_password_hash
from app.utils.types import DTOProtocol

from .base import AbstractBaseRepository


class UserRepository(AbstractBaseRepository[User]):
    model = User

    async def create(self, data: DTOProtocol | dict[str, Any]) -> User:
        unstructured = unstructure(data)
        unstructured.update(
            hashed_password=get_password_hash(unstructured.pop("password"))
        )
        return await super().create(data=unstructured)
