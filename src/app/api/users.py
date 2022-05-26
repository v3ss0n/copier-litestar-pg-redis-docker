from pydantic import UUID4
from starlite import Controller, Provide, Router, delete, get, post, put

from app.config import Paths
from app.models import UserCreateModel, UserModel, UserReadModel
from app.repositories import UserRepository

root_dependencies = {"repository": Provide(UserRepository)}


class UsersController(Controller):
    path = ""

    @post()
    async def create_user(
        self, data: UserCreateModel, repository: UserRepository
    ) -> UserReadModel:
        return await repository.create(data=data)

    @get()
    async def list_users(
        self, repository: UserRepository, offset: int = 0, limit: int = 100
    ) -> list[UserReadModel]:
        return await repository.get_many(offset=offset, limit=limit)


class UserDetailController(Controller):
    path = "{user_id:uuid}"

    @get(cache=True)
    async def get_user(
        self, user_id: UUID4, repository: UserRepository
    ) -> UserReadModel | None:
        return await repository.get_one(instance_id=user_id)

    @put()
    async def update_user(
        self, user_id: UUID4, data: UserModel, repository: UserRepository
    ) -> UserReadModel | None:
        return await repository.partial_update(instance_id=user_id, data=data)

    @delete(status_code=200)
    async def delete_user(
        self, user_id: UUID4, repository: UserRepository
    ) -> UserReadModel:
        return await repository.delete(instance_id=user_id)


user_router = Router(
    path=Paths.USERS,
    route_handlers=[UsersController, UserDetailController],
    dependencies=root_dependencies,
)
