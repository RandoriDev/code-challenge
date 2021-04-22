"""
Randori Code Challenge backend router module.
"""

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


@router.route("/", methods=["GET", "POST", "PUT"])
async def index(request: fastapi.Request) -> fastapi.Response:
    """This function handles requests to the index endpoint, i.e. "/".

    :param request: FastAPI Request instance
    :return: FastAPI Response instance
    """

    if request.method == "GET":
        return fastapi.responses.JSONResponse(content={"message": "Some GET response"}, status_code=200)
    elif request.method == "POST":
        return fastapi.responses.JSONResponse(content={"message": "Some POST response"}, status_code=201)
    else:
        return fastapi.responses.JSONResponse(content={"message": "Some PUT response"}, status_code=202)
