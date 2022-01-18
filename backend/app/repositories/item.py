from app.models import Item

from .base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    pass


item = ItemRepository(Item)
