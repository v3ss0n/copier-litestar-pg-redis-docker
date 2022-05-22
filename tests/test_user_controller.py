from starlette.status import HTTP_201_CREATED
from starlite import TestClient

from app.constants import USER_CONTROLLER_PATH
from tests.factories import UserCreateDTOFactory


def test_create_user(test_client: TestClient) -> None:
    with test_client as client:
        unstructured_user = (
            UserCreateDTOFactory.build().dict()  # type:ignore[attr-defined]
        )
        response = client.post("/v1" + USER_CONTROLLER_PATH, json=unstructured_user)
        print(str(response.text))
        assert response.status_code == HTTP_201_CREATED
