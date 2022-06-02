import logging
from uuid import UUID

from starlite import Controller, Parameter, Provide, Router, delete, get, post, put

from app.config import Paths
from app.models import UserCreateModel, UserModel
from app.repositories import UserRepository
from app.utils import BeforeAfter, LimitOffset

from .utils import CheckPayloadMismatch, filter_for_updated, limit_offset_pagination

logger = logging.getLogger(__name__)

router_dependencies = {"repository": Provide(UserRepository)}


class UsersController(Controller):
    path = ""

    @post(
        operation_id="Create User",
        description="Create a new User by supplying a username and password",
    )
    async def post(
        self, data: UserCreateModel, repository: UserRepository
    ) -> UserModel:
        created_user = await repository.create(data=data)
        logger.info("New User: %s", created_user)
        return created_user

    @get(
        dependencies={
            "limit_offset": Provide(limit_offset_pagination),
            "updated_filter": Provide(filter_for_updated),
        },
        operation_id="List Users",
        description="A paginated list of all Users",
    )
    async def get(
        self,
        repository: UserRepository,
        limit_offset: LimitOffset,
        updated_filter: BeforeAfter,
        is_active: bool = Parameter(query="is-active", default=True),
    ) -> list[UserModel]:
        repository.apply_limit_offset_pagination(limit_offset)
        repository.filter_on_datetime_field(updated_filter)
        return await repository.get_many(is_active=is_active)


class UserDetailController(Controller):
    path = "{user_id:uuid}"

    @get(cache=True, operation_id="Get User", description="Details of a distinct User")
    async def get(self, user_id: UUID, repository: UserRepository) -> UserModel:
        return await repository.get_one(instance_id=user_id)

    @put(
        guards=[CheckPayloadMismatch("id", "user_id").__call__],
        operation_id="Update User",
        description="Modify a distinct User",
    )
    async def update_user(
        self, user_id: UUID, data: UserModel, repository: UserRepository
    ) -> UserModel:
        return await repository.partial_update(instance_id=user_id, data=data)

    @delete(
        status_code=200,
        operation_id="Delete User",
        description="Delete the user and return its representation",
    )
    async def delete(self, user_id: UUID, repository: UserRepository) -> UserModel:
        return await repository.delete(instance_id=user_id)


user_router = Router(
    path=Paths.USERS,
    route_handlers=[UsersController, UserDetailController],
    dependencies=router_dependencies,
    tags=["Users"],
)
