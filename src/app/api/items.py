import logging
from uuid import UUID

from starlite import Controller, Provide, Router, delete, get, post, put

from app.config import Paths
from app.models import ItemCreateModel, ItemModel, UserReadModel
from app.repositories import ItemRepository, UserRepository
from app.utils import BeforeAfter, LimitOffset

from .utils import CheckPayloadMismatch, filter_for_updated, limit_offset_pagination

logger = logging.getLogger(__name__)


async def get_user(user_id: UUID, user_repository: UserRepository) -> UserReadModel:
    return await user_repository.get_one(user_id)


router_dependencies = {
    "repository": Provide(ItemRepository),
    "user_repository": Provide(UserRepository),
    "user": Provide(get_user),
}


class ItemsController(Controller):
    path = ""

    @post()
    async def post(
        self, user: UserReadModel, data: ItemCreateModel, repository: ItemRepository
    ) -> ItemModel:
        created_item = await repository.create_for_user(user=user, data=data)
        logger.info("New Item: %s", created_item)
        return created_item

    @get(
        dependencies={
            "limit_offset": Provide(limit_offset_pagination),
            "updated_filter": Provide(filter_for_updated),
        }
    )
    async def get(
        self,
        user: UserReadModel,
        repository: ItemRepository,
        limit_offset: LimitOffset,
        updated_filter: BeforeAfter,
    ) -> list[ItemModel]:
        repository.apply_limit_offset_pagination(limit_offset)
        repository.filter_on_datetime_field(updated_filter)
        return await repository.get_many_for_user(user=user)


class ItemDetailController(Controller):
    path = "{item_id:uuid}"

    @get(cache=True)
    async def get(
        self, user: UserReadModel, item_id: UUID, repository: ItemRepository
    ) -> ItemModel:
        return await repository.get_one_for_user(user=user, instance_id=item_id)

    @put(
        guards=[
            CheckPayloadMismatch("id", "item_id").__call__,
            CheckPayloadMismatch("owner_id", "user_id").__call__,
        ]
    )
    async def put(
        self,
        user: UserReadModel,
        item_id: UUID,
        data: ItemModel,
        repository: ItemRepository,
    ) -> ItemModel:
        return await repository.partial_update_for_user(
            user=user, instance_id=item_id, data=data
        )

    @delete(status_code=200)
    async def delete(
        self, user: UserReadModel, item_id: UUID, repository: ItemRepository
    ) -> ItemModel:
        return await repository.delete_for_user(user=user, instance_id=item_id)


item_router = Router(
    path=Paths.ITEMS,
    route_handlers=[ItemsController, ItemDetailController],
    dependencies=router_dependencies,
)
