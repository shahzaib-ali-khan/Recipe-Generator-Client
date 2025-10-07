from src.api_client import api_call
from src.config import BASE_URL


def get_recipe_response(model: str, prompt: str) -> str:
    r = api_call(
        f"{BASE_URL}recipes/",
        method="post",
        data={"model": model, "ingredients_as_text": prompt},
    )
    if r.status_code != 200:
        raise Exception(r.text)

    return r.json()["result"]
