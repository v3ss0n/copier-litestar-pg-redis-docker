from uuid import uuid4

import pytest

from app.domain.providers import schema


@pytest.fixture
def provider() -> schema.Provider:
    return schema.Provider(id=uuid4(), name="test provider")
