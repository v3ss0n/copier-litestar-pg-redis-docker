import logging
from uuid import UUID

from starlite import Controller, Parameter, Provide, Router, delete, get, post, put

from app.config import Paths
from app.models import UserCreateModel, UserModel, UserReadModel
from app.repositories import UserRepository

from .utils import (
    BeforeAfter,
    CheckPayloadMismatch,
    LimitOffset,
    filter_for_updated,
    limit_offset_pagination,
)

logger = logging.getLogger(__name__)

router_dependencies = {"repository": Provide(UserRepository)}


class UsersController(Controller):
    path = ""

    @post()
    async def post(
        self, data: UserCreateModel, repository: UserRepository
    ) -> UserReadModel:
        created_user = await repository.create(data=data)
        logger.info("New User: %s", created_user)
        return created_user

    @get(
        dependencies={
            "limit_offset": Provide(limit_offset_pagination),
            "updated_filter": Provide(filter_for_updated),
        }
    )
    async def get(
        self,
        repository: UserRepository,
        limit_offset: LimitOffset,
        updated_filter: BeforeAfter,
        is_active: bool = Parameter(query="is-active", default=True),
    ) -> list[UserReadModel]:
        repository.apply_limit_offset_pagination(limit_offset)
        repository.filter_on_datetime_field(updated_filter)
        return await repository.get_many(is_active=is_active)


class UserDetailController(Controller):
    path = "{user_id:uuid}"

    @get(cache=True)
    async def get(self, user_id: UUID, repository: UserRepository) -> UserReadModel:
        return await repository.get_one(instance_id=user_id)

    @put(guards=[CheckPayloadMismatch("id", "user_id").__call__])
    async def put(
        self, user_id: UUID, data: UserModel, repository: UserRepository
    ) -> UserReadModel:
        return await repository.partial_update(instance_id=user_id, data=data)

    @delete(status_code=200)
    async def delete(self, user_id: UUID, repository: UserRepository) -> UserReadModel:
        return await repository.delete(instance_id=user_id)


user_router = Router(
    path=Paths.USERS,
    route_handlers=[UsersController, UserDetailController],
    dependencies=router_dependencies,
)
