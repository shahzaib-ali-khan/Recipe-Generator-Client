from src.api_client import api_call
from src.config import BASE_URL


def get_recipe_response(model: str, prompt: str) -> str:
    try:
        r = api_call(
            f"{BASE_URL}recipes/",
            method="post",
            data={"model": model, "ingredients_as_text": prompt},
        )
        return r.json().get("result", "No response")
    except Exception as e:
        return f"⚠️ Error contacting server: {e}"
