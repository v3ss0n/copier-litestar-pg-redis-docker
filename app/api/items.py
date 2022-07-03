import logging
from uuid import UUID

from starlite import Controller, Provide, Router, delete, get, post, put

from app.config import Paths
from app.models import ItemCreateModel, ItemModel, UserModel
from app.repositories import ItemRepository, UserRepository

from .utils import CheckPayloadMismatch, filter_for_updated, limit_offset_pagination

logger = logging.getLogger(__name__)


async def get_user(user_id: UUID, user_repository: UserRepository) -> UserModel:
    """
    Get user representation.

    Parameters
    ----------
    user_id : UUID
    user_repository : UserRepository

    Returns
    -------
    UserModel
    """
    return await user_repository.get_one(user_id)


router_dependencies = {
    "repository": Provide(ItemRepository),
    "user_repository": Provide(UserRepository),
    "user": Provide(get_user),
}


class ItemsController(Controller):
    path = ""
    tags = ["User-Items"]

    @post(
        description="Create a new Item for the User by supplying the Item's name",
    )
    async def create_user_item(
        self, user: UserModel, data: ItemCreateModel, repository: ItemRepository
    ) -> ItemModel:
        """
        Create a new Item for the User.
        """
        created_item = await repository.create_for_user(user=user, data=data)
        logger.info("New Item: %s", created_item)
        return created_item

    @get(
        dependencies={
            "limit_offset": Provide(limit_offset_pagination),
            "updated_filter": Provide(filter_for_updated),
        },
        description="A paginated list of all Items belonging to the User",
    )
    async def list_user_items(
        self,
        user: UserModel,
        repository: ItemRepository,
    ) -> list[ItemModel]:
        """
        Paginated list of User's Items.
        """
        return await repository.get_many_for_user(user=user)


class ItemDetailController(Controller):
    path = "{item_id:uuid}"
    tags = ["User-Items"]

    @get(
        cache=True,
        description="Details of a distinct Item belonging to the User",
    )
    async def get_user_item(
        self, user: UserModel, item_id: UUID, repository: ItemRepository
    ) -> ItemModel:
        """
        User Item member view.
        """
        return await repository.get_one_for_user(user=user, instance_id=item_id)

    @put(
        guards=[
            CheckPayloadMismatch("id", "item_id").__call__,
            CheckPayloadMismatch("owner_id", "user_id").__call__,
        ],
        description="Modify the User's Item.",
    )
    async def update_user_item(
        self,
        user: UserModel,
        item_id: UUID,
        data: ItemModel,
        repository: ItemRepository,
    ) -> ItemModel:
        """
        Update User Item member
        """
        return await repository.partial_update_for_user(
            user=user, instance_id=item_id, data=data
        )

    @delete(
        status_code=200,
        description="Delete the User's Item and return its representation",
    )
    async def delete_user_item(
        self, user: UserModel, item_id: UUID, repository: ItemRepository
    ) -> ItemModel:
        """
        Delete User Item member.
        """
        return await repository.delete_for_user(user=user, instance_id=item_id)


item_router = Router(
    path=Paths.ITEMS,
    route_handlers=[ItemsController, ItemDetailController],
    dependencies=router_dependencies,
)
