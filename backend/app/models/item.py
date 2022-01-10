from typing import Optional, Union, Dict, ForwardRef

import ormar

from .base import Base, BaseMeta
from .user import User, UserDB


class Item(Base):
    class Meta(BaseMeta):
        tablename = "items"

    name: str = ormar.String(max_length=50, unique=True, index=True)
    # owner: Optional[Union[User, Dict]] = ormar.ForeignKey(
    #     UserDB,
    #     related_name="items",
    # )
