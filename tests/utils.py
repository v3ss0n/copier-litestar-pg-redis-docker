from requests import Response


def check_response(response: Response, expected_status: int) -> None:
    if response.status_code != expected_status:
        print(str(response.text))
        raise RuntimeError(
            f"Response status code ({response.status_code}) does not equal expected "
            f"({expected_status})"
        )
