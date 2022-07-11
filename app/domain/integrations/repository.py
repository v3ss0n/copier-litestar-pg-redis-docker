from app import core

from . import model


class Repository(core.Repository[model.Integration]):
    model_type = model.Integration
