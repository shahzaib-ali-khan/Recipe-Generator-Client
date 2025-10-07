from src.api_client import api_call
from src.config import BASE_URL


def get_available_llms() -> list[str] | str:
    try:
        r = api_call(
            f"{BASE_URL}supported_llms/",
            method="get",
            data=None,
        )
        return r.json().get("result", "No response")
    except Exception as e:
        return f"⚠️ Error contacting server: {e}"
