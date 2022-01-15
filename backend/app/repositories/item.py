from .base import BaseRepository
from app.models import Item


class ItemRepository(BaseRepository[Item]):
    pass


item = ItemRepository(Item)
