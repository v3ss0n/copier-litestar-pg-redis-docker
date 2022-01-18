from app.models import Item

from .base import AbstractBaseRepository


class ItemRepository(AbstractBaseRepository[Item]):
    model = Item
