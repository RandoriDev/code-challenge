"""
Randori Code Challenge main router module.
"""

import asyncio
import os
from typing import Optional, Tuple

import fastapi

from code_challenge import constants
from code_challenge.services import proxy
from code_challenge.utils import duplicate, hashing, malicious

# create an instance of the Router so that we can use it's decorator methods with the API methods
router = fastapi.APIRouter()


def register_router(api: fastapi.FastAPI):
    """This function registers the instance of the proxy router with the given API instance.

    :param api: FastAPI API instance
    """

    api.include_router(router=router)


async def is_malicious(request: fastapi.Request) -> bool:
    """This function determines whether a request payload is malicious.

    :param request: FastAPI Request instance
    :return: Whether the given request instance's payload is malicious
    """

    # get the payload
    payload = await request.json()

    if payload:
        return malicious.is_malicious(payload=payload)

    return False


def get_request_client_host_and_hash(request: fastapi.Request) -> Tuple[str, str]:
    """This function determines whether a request is a duplicate.

    :param request: FastAPI Request instance
    :return: Whether a request is a duplicate
    """

    # get the string representation of the request object
    request_str = str(request)

    # get the client host to ensure that this request is not coming from another client
    client_host = request.client.host

    # get the hash of the request
    request_hash = hashing.hash_object(obj=request_str)

    return client_host, request_hash


def is_duplicate_request(request: fastapi.Request) -> bool:
    """This function determines whether a request is a duplicate.

    :param request: FastAPI Request instance
    :return: Whether a request is a duplicate
    """

    # get the client host and request hash
    client_host, request_hash = get_request_client_host_and_hash(request=request)

    # return whether this is a duplicate request
    return duplicate.is_duplicate(client_host=client_host, request_hash=request_hash)


async def make_proxy_request(
    request: fastapi.Request,
    backend_url: str,
    backend_port: int,
    is_duplicate_request: bool,
) -> Tuple[int, dict, dict]:
    """This function will proxy a request to a given backend URL and port.

    :param request: FastAPI Request instance
    :param backend_url: Backend URL to proxy the request to
    :param backend_port: Backend port to proxy the request to
    :param is_duplicate_request: Whether this is a duplicate request
    :return: Tuple containing the response status code and JSON data payload
    :raise: CodeChallengeProxyRequestError: If a proxy request failed
    """

    if is_duplicate_request:
        # sleep using asyncio.sleep(), which will not block, unlike time.sleep()
        await asyncio.sleep(delay=constants.IS_DUPLICATE_DELAY)

    request_method = request.method

    # get the client host and request hash
    client_host, request_hash = get_request_client_host_and_hash(request=request)

    if request_method != "GET":
        request_payload = await request.body()
    else:
        request_payload = None

    try:
        return await proxy.proxy_request(
            request_method=request_method,
            backend_url=backend_url,
            backend_port=backend_port,
            request_payload=request_payload,
        )
    except proxy.CodeChallengeProxyRequestError as e:
        raise e
    finally:
        # in Python, the finally block will be executed before the exception raise
        duplicate.persist_request_hash(client_host=client_host, request_hash=request_hash)


@router.route("/", methods=["GET", "POST", "PUT"])
async def index(request: fastapi.Request) -> fastapi.Response:
    """This function handles requests to the index endpoint, i.e. "/".

    :param request: FastAPI Request instance
    :return: FastAPI Response instance
    """

    # get env vars
    backend_url = os.getenv(constants.ENV_BACKEND_URL)
    backend_port = os.getenv(constants.ENV_BACKEND_PORT)

    # define an empty response that will be returned if there is no errors
    response_content = ""

    # check whether the request method is POST
    if request.method == "POST":
        # check for a malicious request
        if await is_malicious(request=request):
            return fastapi.responses.JSONResponse(status_code=401, content={"error": "Malicious request detected!"})

    is_duplicate = is_duplicate_request(request=request)

    response_status_code, response_json = await make_proxy_request(
        request=request,
        backend_url=backend_url,
        backend_port=backend_port,
        is_duplicate_request=is_duplicate,
    )

    return fastapi.responses.JSONResponse(status_code=response_status_code, content=response_json)
