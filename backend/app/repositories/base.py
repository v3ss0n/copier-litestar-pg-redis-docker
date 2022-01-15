from typing import Generic, TypeVar, Type, Any, Optional, List, Union, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base import Base
from app.db.session import get_db

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
    ):
        # self.database = ModelType.Meta.database
        self.model = model

    async def get(self, id: Any, db: Session = get_db) -> Optional[ModelType]:
        obj = await db.execute(select(ModelType).where(ModelType.id == id)).first()
        return obj

    async def get_multi(
        self, *, offset: int = 0, limit: int = 100, db: Session = get_db
    ) -> List[ModelType]:
        objs = await db.execute(select(ModelType).offset(offset).limit(limit)).all()
        return objs

    async def create(self, db_obj: ModelType) -> Optional[ModelType]:
        try:
            await db_obj.save()
            return db_obj
        except:
            raise Exception  # todo

    async def update(self, id: Any, obj_in: Union[ModelType, Dict[str, Any]]):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        db_obj = await self.read_type.objects.get(id=id)
        updated_obj = await db_obj.update(**update_data)
        return updated_obj

    async def delete(self, id: Any) -> Optional[ModelType]:
        db_obj = await self.model.objects.get(id=id)
        db_obj = await db_obj.delete()
        return db_obj
