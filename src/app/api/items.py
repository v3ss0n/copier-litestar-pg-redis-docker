from uuid import UUID

from starlite import Controller, Provide, Router, delete, get, post, put

from app.config import Paths
from app.models import ItemCreateModel, ItemModel, UserReadModel
from app.repositories import ItemRepository, UserRepository

from .utils import CheckPayloadMismatch


async def get_user(user_id: UUID, user_repository: UserRepository) -> UserReadModel:
    return await user_repository.get_one(user_id)


root_dependencies = {
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
        return await repository.create_for_user(user=user, data=data)

    @get()
    async def get(
        self,
        user: UserReadModel,
        repository: ItemRepository,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ItemModel]:
        return await repository.get_many_for_user(user=user, offset=offset, limit=limit)


class ItemDetailController(Controller):
    path = "{item_id:uuid}"

    @get(cache=True)
    async def get(
        self, user: UserReadModel, item_id: UUID, repository: ItemRepository
    ) -> ItemModel | None:
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
    ) -> ItemModel | None:
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
    dependencies=root_dependencies,
)
