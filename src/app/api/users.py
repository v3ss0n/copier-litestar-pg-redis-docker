from uuid import UUID

from starlite import Controller, Provide, Router, delete, get, post, put

from app.config import Paths
from app.models import UserCreateModel, UserModel, UserReadModel
from app.repositories import UserRepository

from .utils import CheckPayloadMismatch

root_dependencies = {"repository": Provide(UserRepository)}


class UsersController(Controller):
    path = ""

    @post()
    async def post(
        self, data: UserCreateModel, repository: UserRepository
    ) -> UserReadModel:
        return await repository.create(data=data)

    @get()
    async def get(
        self, repository: UserRepository, offset: int = 0, limit: int = 100
    ) -> list[UserReadModel]:
        return await repository.get_many(offset=offset, limit=limit)


class UserDetailController(Controller):
    path = "{user_id:uuid}"

    @get(cache=True)
    async def get(
        self, user_id: UUID, repository: UserRepository
    ) -> UserReadModel | None:
        return await repository.get_one(instance_id=user_id)

    @put(guards=[CheckPayloadMismatch("id", "user_id").__call__])
    async def put(
        self, user_id: UUID, data: UserModel, repository: UserRepository
    ) -> UserReadModel | None:
        return await repository.partial_update(instance_id=user_id, data=data)

    @delete(status_code=200)
    async def delete(self, user_id: UUID, repository: UserRepository) -> UserReadModel:
        return await repository.delete(instance_id=user_id)


user_router = Router(
    path=Paths.USERS,
    route_handlers=[UsersController, UserDetailController],
    dependencies=root_dependencies,
)
