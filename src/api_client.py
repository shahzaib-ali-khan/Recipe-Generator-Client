import time

import requests
import structlog
from requests import ConnectionError, RequestException, Response, Timeout

logger = structlog.get_logger(__name__)
MAX_RETRIES = 3
BASE_BACKOFF = 2
TIMEOUT = 10


def api_call(
    url: str,
    method: str = "post",
    data: dict = None,
) -> Response:
    extra_args = {}
    if method == "post":
        extra_args = {"json": data}

    retries = 0
    while retries <= MAX_RETRIES:
        try:
            response = getattr(requests, method)(
                url,
                **extra_args,
            )
            return response
        except RequestException as exc:
            wait_time = 2**retries
            logger.error(
                f"Error fetching {url}: {exc}. Retry {retries + 1}/{MAX_RETRIES} in {wait_time}s"
            )
            time.sleep(wait_time)
        except ValueError as exc:
            logger.error(f"Value error in {url}: {exc}")
            raise
        except (Timeout, ConnectionError) as exc:
            wait_time = BASE_BACKOFF**retries
            logger.warning(
                f"Transient error calling {url}: {exc}. Retry {retries + 1}/{MAX_RETRIES} in {wait_time}s"
            )
            time.sleep(wait_time)

        retries += 1
        if retries >= MAX_RETRIES:
            logger.error(f"Max retries reached for {url}. Failing permanently.")
            raise

    raise RuntimeError("api_call failed unexpectedly")
