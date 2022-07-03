from typing import Any
from uuid import UUID

from app.models.item import Item, ItemModel
from app.models.user import UserModel
from app.utils.types import SupportsDict

from .base import AbstractBaseRepository


class ItemRepository(AbstractBaseRepository[Item, ItemModel]):
    db_model = Item
    return_model = ItemModel

    def filter_for_user(self, user: UserModel) -> None:
        """
        Apply filter for user id to query.

        Parameters
        ----------
        user : UserModel
        """
        self.base_select = self.base_select.where(Item.owner_id == user.id)

    async def get_many_for_user(
        self, user: UserModel, **kwargs: Any
    ) -> list[ItemModel]:
        """
        A list of `ItemModel` instances.

        Parameters
        ----------
        user : UserReadModel
            Representation of the user that owns the items.
        **kwargs : any
            each key/value pair added to where-clause of query as ``<key> == <value>``.

        Returns
        -------
        list[ItemModel]
        """
        self.filter_for_user(user)
        return await self.get_many(**kwargs)

    async def get_one_for_user(self, user: UserModel, instance_id: UUID) -> ItemModel:
        """
        Get a user's item.

        Parameters
        ----------
        user : UserModel
        instance_id : UUID

        Returns
        -------
        ItemModel
        """
        self.filter_for_user(user)
        return await self.get_one(instance_id)

    async def create_for_user(self, user: UserModel, data: SupportsDict) -> ItemModel:
        """
        Create an item for user.

        Parameters
        ----------
        user : UserModel
        data : SupportsDict

        Returns
        -------
        ItemModel
        """
        instance = await self._add_flush_refresh(
            self.db_model(owner_id=user.id, **data.dict())
        )
        return self.return_model.from_orm(instance)

    async def partial_update_for_user(
        self, user: UserModel, instance_id: UUID, data: SupportsDict
    ) -> ItemModel:
        """
        Update a user's items.

        Parameters
        ----------
        user : UserModel
        instance_id : UUID
        data : SupportsDict

        Returns
        -------
        ItemModel
        """
        self.filter_for_user(user)
        return await self.partial_update(instance_id, data)

    async def delete_for_user(self, user: UserModel, instance_id: UUID) -> ItemModel:
        """
        Delete user's item.

        Parameters
        ----------
        user : UserModel
        instance_id : UUID

        Returns
        -------
        ItemModel
        """
        self.filter_for_user(user)
        return await self.delete(instance_id)
