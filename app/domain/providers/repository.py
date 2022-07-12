from app import core

from . import model


class Repository(core.Repository[model.Provider]):
    model_type = model.Provider
