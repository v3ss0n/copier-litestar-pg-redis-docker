from typing import Any
from unittest.mock import ANY

import pytest
from starlette import status
from starlite import TestClient

from app.constants import USER_CONTROLLER_PATH

from .utils import check_response


@pytest.fixture
def unstructured_user() -> dict[str, Any]:
    return {
        "username": "Rick Sanchez",
        "is_active": True,
        "password": "wubbalubbadubdub",
    }


def test_create_user(
    unstructured_user: dict[str, str], test_client: TestClient
) -> None:
    with test_client as client:
        response = client.post("/v1" + USER_CONTROLLER_PATH, json=unstructured_user)
        check_response(response, status.HTTP_201_CREATED)
        assert response.json() == {
            "id": ANY,
            "username": "Rick Sanchez",
            "is_active": True,
        }


def test_create_user_invalid_payload(
    unstructured_user: dict[str, str], test_client: TestClient
) -> None:
    del unstructured_user["password"]
    with test_client as client:
        response = client.post("/v1" + USER_CONTROLLER_PATH, json=unstructured_user)
        check_response(response, status.HTTP_400_BAD_REQUEST)
