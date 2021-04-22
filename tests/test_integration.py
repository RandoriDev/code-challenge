"""
Randori Code Challenge integration tests module.

NOTE: Server and backend server must be running first!!!
"""

import logging
import os
from typing import Optional

import dotenv
import httpx
import pytest

from code_challenge import constants, log


async def make_http_call(
    request_method: str, url: str, logger: logging.Logger, request_payload: Optional[dict] = None
) -> httpx.Response:
    """This function makes an HTTP call.

    :param request_method: HTTP request method
    :param url: URL
    :param logger: Logger instance
    :param request_payload: Optional request payload
    :return: httpx Response object
    """

    async with httpx.AsyncClient() as client:
        # log message
        logger.info(f"Making {request_method} call")

        if request_method == "GET":
            # just forward request without any payload
            response = await client.request(method=request_method, url=url)
        else:
            response = await client.request(method=request_method, url=url, json=request_payload)

        # log message
        logger.info(f"Received response")

        return response


@pytest.fixture(scope="module")
def logger() -> logging.Logger:
    """Get a module level logger."""

    log.initialize_app_logger(constants.TESTS_APP_NAME)
    return logging.getLogger(constants.TESTS_APP_NAME)


@pytest.fixture(scope="module")
def env():
    """Load environment variables."""

    # load dotenv
    dotenv.load_dotenv()


@pytest.fixture(scope="module")
def server_url(env) -> str:
    """Create the server URL."""

    return f"http://{os.getenv(constants.ENV_HOST)}:{os.getenv(constants.ENV_PORT)}"


@pytest.mark.parametrize("expected_status_code", [200, 200])
@pytest.mark.asyncio
async def test_get(server_url: str, logger: logging.Logger, expected_status_code: int):
    """Test the HTTP GET method."""

    response = await make_http_call(request_method="GET", url=server_url, logger=logger)

    assert response
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "payload, expected_status_code, expected_content",
    [
        ({"key": "value"}, 201, {"message": "Some POST response"}),
        ({"is_malicious": True}, 401, {"error": "Malicious request detected!"}),
    ],
)
@pytest.mark.asyncio
async def test_post(
    server_url: str, logger: logging.Logger, payload: dict, expected_status_code: int, expected_content: dict
):
    """Test the HTTP POST method."""

    response = await make_http_call(request_method="POST", url=server_url, logger=logger, request_payload=payload)

    assert response
    assert response.status_code == expected_status_code
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "payload, expected_status_code, expected_content",
    [
        ({"key": "value"}, 202, {"message": "Some PUT response"}),
    ],
)
@pytest.mark.asyncio
async def test_put(
    server_url: str, logger: logging.Logger, payload: dict, expected_status_code: int, expected_content: dict
):
    """Test the HTTP PUT method."""

    response = await make_http_call(request_method="PUT", url=server_url, logger=logger, request_payload=payload)

    assert response
    assert response.status_code == expected_status_code
    assert response.json() == expected_content
