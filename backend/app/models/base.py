from pydantic import UUID4

import ormar
import uuid

from app.db.session import SessionLocal
from app.db.db import database, metadata
from .mixins import DateFieldsMixins


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class Base(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        abstract = True

    id: UUID4 = ormar.String(primary_key=True, default=uuid.uuid4, max_length=32)
