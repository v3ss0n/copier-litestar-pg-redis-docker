from uuid import UUID

from app.models.item import Item, ItemModel
from app.models.user import UserReadModel
from app.utils.types import SupportsDict

from .base import AbstractBaseRepository


class ItemRepository(AbstractBaseRepository[Item, ItemModel]):
    db_model = Item
    return_model = ItemModel

    def filter_for_user(self, user: UserReadModel) -> None:
        self.base_select = self.base_select.where(Item.owner_id == user.id)

    async def get_many_for_user(
        self, user: UserReadModel, offset: int = 0, limit: int = 100
    ) -> list[ItemModel]:
        self.filter_for_user(user)
        return await self.get_many(offset=offset, limit=limit)

    async def get_one_for_user(
        self, user: UserReadModel, instance_id: UUID
    ) -> ItemModel:
        self.filter_for_user(user)
        return await self.get_one(instance_id)

    async def create_for_user(
        self, user: UserReadModel, data: SupportsDict
    ) -> ItemModel:
        instance = await self._add_flush_refresh(
            self.db_model(owner_id=user.id, **data.dict())
        )
        return self.return_model.from_orm(instance)

    async def partial_update_for_user(
        self, user: UserReadModel, instance_id: UUID, data: SupportsDict
    ) -> ItemModel:
        self.filter_for_user(user)
        return await self.partial_update(instance_id, data)

    async def delete_for_user(
        self, user: UserReadModel, instance_id: UUID
    ) -> ItemModel:
        self.filter_for_user(user)
        return await self.delete(instance_id)
