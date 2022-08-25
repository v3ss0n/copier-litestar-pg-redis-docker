from pydantic import BaseModel


class Schema(BaseModel):
    """Base for all Pydantic models.

    Have not included the `id` attribute that is included in the
    SQLAlchemy `Base` as that would force it to be available to all
    create and read models. Therefore, where a resource representation
    should include the `id` field, it must be added in the subclass.
    """

    class Config:
        extra = "ignore"
        arbitrary_types_allowed = True
        orm_mode = True
