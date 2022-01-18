from starlette.status import HTTP_201_CREATED
from starlite import TestClient

from app.constants import USER_CONTROLLER_PATH
from tests.factories import UserCreateDTOFactory


def test_create_user(test_client: TestClient):
    create_user_dto = UserCreateDTOFactory.build().dict()
    response = test_client.post("/v1" + USER_CONTROLLER_PATH, json=create_user_dto)
    assert response.status_code == HTTP_201_CREATED