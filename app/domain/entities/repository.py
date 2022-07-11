from app import core

from . import model


class Repository(core.Repository[model.Entity]):
    model_type = model.Entity
