from datetime import datetime
from typing import Any
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
        self,
        user: UserReadModel,
        offset: int,
        limit: int,
        updated_before: datetime | None,
        updated_after: datetime | None,
        **kwargs: Any,
    ) -> list[ItemModel]:
        """
        A list of `ItemModel` instances.

        Parameters
        ----------
        user : UserReadModel
            Representation of the user that owns the items.
        offset : int
            For limit/offset pagination.
        limit : int
            For limit/offset pagination.
        updated_before : datetime
            Return only records that have been updated after `datetime`.
        updated_after : datetime
            Return only records that have been updated before `datetime`.
        **kwargs : any
            each key/value pair added to where-clause of query as ``<key> == <value>``.

        Returns
        -------
        list[ItemModel]
        """
        self.filter_for_user(user)
        return await self.get_many(
            offset=offset,
            limit=limit,
            updated_before=updated_before,
            updated_after=updated_after,
            **kwargs,
        )

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
