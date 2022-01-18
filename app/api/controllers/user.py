from pydantic import UUID4
from starlite import Controller, delete, get, post, put

from app.models import UserCreate, UserRead
from app.repositories import UserRepository


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: UserCreate) -> UserRead | None:
        return await UserRepository.create(data=data)

    @get()
    async def list_users(self, offset: int = 0, limit: int = 100) -> list[UserRead]:
        return await UserRepository.get_many(offset=offset, limit=limit)

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4) -> UserRead | None:
        return await UserRepository.get_one(instance_id=user_id)

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: UserCreate) -> UserRead | None:
        return await UserRepository.partial_update(instance_id=user_id, data=data)

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> UserRead | None:
        return await UserRepository.delete(instance_id=user_id)
