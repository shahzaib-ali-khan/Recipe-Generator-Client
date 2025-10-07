from src.api_client import api_call
from src.config import BASE_URL


def get_available_llms() -> list[str] | str:
    r = api_call(
        f"{BASE_URL}supported_llms/",
        method="get",
        data=None,
    )
    if r.status_code != 200:
        raise Exception(r.text)

    return r.json()["result"]
