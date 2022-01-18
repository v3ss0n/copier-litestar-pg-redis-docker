from pydantic import UUID4
from starlite import Controller, delete, get, post, put

from app.constants import USER_CONTROLLER_PATH
from app.models import UserCreateDTO, UserReadDTO
from app.repositories import UserRepository


class UserController(Controller):
    path = USER_CONTROLLER_PATH

    @post()
    async def create_user(self, data: UserCreateDTO) -> UserReadDTO | None:
        return await UserRepository.create(data=data)

    @get()
    async def list_users(self, offset: int = 0, limit: int = 100) -> list[UserReadDTO]:
        return await UserRepository.get_many(offset=offset, limit=limit)

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4) -> UserReadDTO | None:
        return await UserRepository.get_one(instance_id=user_id)

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: UserCreateDTO) -> UserReadDTO | None:
        return await UserRepository.partial_update(instance_id=user_id, data=data)

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> UserReadDTO | None:
        return await UserRepository.delete(instance_id=user_id)
