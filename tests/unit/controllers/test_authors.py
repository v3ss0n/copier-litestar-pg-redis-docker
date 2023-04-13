from typing import TYPE_CHECKING
from unittest.mock import ANY

from litestar.status_codes import HTTP_200_OK

if TYPE_CHECKING:
    import pytest
    from litestar.testing import TestClient


def test_list_authors(client: "TestClient") -> None:
    response = client.get("/v1/authors")
    assert response.status_code == HTTP_200_OK
    assert response.json() == [
        {
            "name": "Agatha Christie",
            "dob": "1890-09-15",
            "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
            "created": "0001-01-01T00:00:00",
            "updated": "0001-01-01T00:00:00",
            "nationality": None,
        },
        {
            "name": "Leo Tolstoy",
            "dob": "1828-09-09",
            "id": "5ef29f3c-3560-4d15-ba6b-a2e5c721e4d2",
            "created": "0001-01-01T00:00:00",
            "updated": "0001-01-01T00:00:00",
            "nationality": None,
        },
    ]


def test_create_author(client: "TestClient", monkeypatch: "pytest.MonkeyPatch") -> None:
    response = client.post("/v1/authors", json={"name": "James Patterson", "dob": "1974-03-22", "nationality": None})
    response_json = response.json()
    assert response_json == {
        "id": ANY,
        "created": ANY,
        "updated": ANY,
        "name": "James Patterson",
        "dob": "1974-03-22",
        "nationality": None,
    }


def test_get_author(client: "TestClient") -> None:
    response = client.get("/v1/authors/97108ac1-ffcb-411d-8b1e-d9183399f63b")
    assert response.json() == {
        "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
        "created": "0001-01-01T00:00:00",
        "updated": "0001-01-01T00:00:00",
        "name": "Agatha Christie",
        "dob": "1890-09-15",
        "nationality": None,
    }


def test_update_author(client: "TestClient") -> None:
    response = client.put(
        "/v1/authors/97108ac1-ffcb-411d-8b1e-d9183399f63b",
        json={
            "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
            "created": "0001-01-01T00:00:00",
            "updated": "0001-01-01T00:00:00",
            "name": "A. Christie",
            "dob": "1890-09-15",
            "nationality": None,
        },
    )
    assert response.json() == {
        "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
        "created": "0001-01-01T00:00:00",
        "updated": ANY,
        "name": "A. Christie",
        "dob": "1890-09-15",
        "nationality": None,
    }


def test_delete_author(client: "TestClient") -> None:
    response = client.delete("/v1/authors/97108ac1-ffcb-411d-8b1e-d9183399f63b")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
        "created": "0001-01-01T00:00:00",
        "updated": "0001-01-01T00:00:00",
        "name": "Agatha Christie",
        "dob": "1890-09-15",
        "nationality": None,
    }
