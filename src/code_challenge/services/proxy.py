"""
Randori Code Challenge proxy service module.
"""

import asyncio
from typing import Optional, Tuple

import fastapi
import httpx  # We could use httpx, aiohttp, or requests with asyncio


class CodeChallengeProxyRequestError(Exception):
    """This class represents an issue with a proxy request."""

    def __init__(self, message: str, status_code: int):
        Exception.__init__(self, message)
        self.status_code = status_code


async def proxy_request(
    request_method: str,
    backend_url: str,
    backend_port: int,
    request_payload: Optional[bytes] = None,
) -> Tuple[int, dict]:
    """This function will proxy a request to a given backend URL and port.

    :param request_method: Request method
    :param backend_url: Backend URL to proxy the request to
    :param backend_port: Backend port to proxy the request to
    :param request_payload: Optional payload to send with the proxied request
    :param delay: Optional number of seconds to delay the proxy request by
    :return: Tuple containing the response status code and data payload as a dictionary
    :raise: CodeChallengeProxyRequestError: If a proxy request failed
    """

    url = f"{backend_url}:{backend_port}"
    response_data = ""

    async with httpx.AsyncClient() as client:
        if request_method == "GET":
            # just forward request without any payload
            response = await client.request(method=request_method, url=url)
        else:
            response = await client.request(method=request_method, url=url, data=request_payload)

        if response.status_code >= 300:
            # there was an error
            raise CodeChallengeProxyRequestError(message=response.text, status_code=response.status_code)

    # we will assume that the response will always return some JSON data
    response_json = response.json()

    # we will assume that we do not need to return HTTP headers
    return response.status_code, response_json
