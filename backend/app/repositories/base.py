from typing import Generic, TypeVar, Type, Any, Optional, List, Union, Dict
from pydantic.main import Model

from sqlalchemy.orm import Session
import uuid

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
DBType = TypeVar("DBType", bound=Base)


class BaseRepository(Generic[ModelType, DBType]):
    def __init__(self, model: Type[ModelType], db_model: Optional[DBType]):
        self.database = ModelType.Meta.database
        self.model = model
        if DBType:
            self.db_model = db_model
        else:
            self.db_model = model

    @self.database.transaction()  # todo: best way to handle this? unsure how to pass transaction decorator around; also seems repetative
    async def get(self, id: Any) -> Optional[ModelType]:
        obj = await ModelType.objects.get(id=id)
        return obj

    @self.database.transaction()
    async def get_multi(self, *, offset: int = 0, limit: int = 100) -> List[ModelType]:
        objs = await ModelType.offset(offset).limit(limit).all()
        return objs

    @self.database.transaction()
    async def create(self, db_obj: DBType) -> Optional[ModelType]:
        try:
            await db_obj.save()
            return db_obj
        except:
            raise Exception  # todo

    @self.database.transaction()
    async def update(self, id: Any, obj_in: Union[ModelType, Dict[str, Any]]):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        updated_obj = await ModelType.objects.get(id=id).update(**update_data)
        return updated_obj

    @self.database.transaction()
    async def delete(self, id: Any) -> Optional[ModelType]:
        obj = await ModelType.objects.get(id=id).delete()
        return obj
