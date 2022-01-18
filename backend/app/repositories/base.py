from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.db.session import get_db
from app.models.base import Base
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
    ):
        self.model = model

    async def get(self, id: Any, db: Session = get_db) -> Optional[ModelType]:
        obj = await db.execute(select(ModelType).where(ModelType.id == id)).first()
        return obj

    async def get_multi(self, *, offset: int = 0, limit: int = 100, db: Session = get_db) -> List[ModelType]:
        objs = await db.execute(select(ModelType).offset(offset).limit(limit)).all()
        return objs

    async def create(self, obj_in: ModelType, db: Session = get_db) -> Optional[ModelType]:
        try:
            obj = self.model(**obj_in)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except:
            raise Exception  # todo

    async def update(
        self, id: Any, obj_in: Union[ModelType, Dict[str, Any]], db: Session = get_db
    ) -> Optional[ModelType]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        db_obj = await self.get(id=id)
        for field in db_obj:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        db.add(obj_in)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def delete(self, id: Any, db: Session = get_db) -> Optional[ModelType]:
        db_obj = await self.get(id=id)
        db.delete(db_obj)
        db.commit()
        return db_obj
