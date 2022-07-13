import re
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, MetaData
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped
from sqlalchemy.orm.decl_api import as_declarative, declared_attr

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
meta = MetaData(naming_convention=convention)


@as_declarative(metadata=meta)
class Base:
    """
    Base for all SQLAlchemy declarative models.
    """

    __name__: str

    table_name_pattern = re.compile(r"(?<!^)(?=[A-Z])")

    # noinspection PyMethodParameters
    @declared_attr
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return re.sub(cls.table_name_pattern, "_", cls.__name__).lower()

    id: Mapped[UUID] = Column(pg.UUID, default=uuid4, primary_key=True)
    created_date: Mapped[datetime] = Column(DateTime, default=datetime.now, nullable=False)
    updated_date: Mapped[datetime] = Column(DateTime, default=datetime.now, nullable=False)
