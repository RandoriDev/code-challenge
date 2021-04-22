"""
Randori Code Challenge server module.
"""

import logging
import os
import time
from typing import Any
import uuid

import dotenv
import fastapi
import uvicorn

from code_challenge import constants, log
from code_challenge.routers import main


class CodeChallengeInitializationError(RuntimeError):
    pass


# create an instance of the Api so that we can use it's decorator method to create the logger middleware
api = fastapi.FastAPI()


def check_env():
    """This function checks that specific environment variables have been provided.

    :raise: CodeChallengeInitializationError: If one or more environment variables were not set
    """

    errors = []

    if not os.getenv(constants.ENV_HOST):
        errors.append(f"{constants.ENV_HOST} must be provided as an environment variable")

    if not os.getenv(constants.ENV_PORT):
        errors.append(f"{constants.ENV_PORT} must be provided as an environment variable")

    if not os.getenv(constants.ENV_BACKEND_URL):
        errors.append(f"{constants.ENV_BACKEND_URL} must be provided as an environment variable")

    if not os.getenv(constants.ENV_BACKEND_PORT):
        errors.append(f"{constants.ENV_BACKEND_PORT} must be provided as an environment variable")

    if errors:
        logger = logging.getLogger(constants.APP_NAME)
        for error in errors:
            logger.error(error)

        raise CodeChallengeInitializationError(
            "Server could not start due to startup errors. See event log for more detail."
        )


@api.middleware("http")
async def log_requests(request: fastapi.Request, call_next: Any):
    """This function acts as a request logger middleware.

    :param request: Request
    :param call_next: Function to call after logging the request
    """

    # get logger
    logger = logging.getLogger(constants.APP_NAME)

    # create new uuid4
    uuid_id = uuid.uuid4()

    # log message
    logger.info(f"Processing request {uuid_id} for method {request.method} and path {request.url.path}")

    # record start time
    start_time = time.time()

    # invoke call_next
    response = await call_next(request)

    # get the elapsed time in milliseconds
    time_elapsed = (time.time() - start_time) * 1000

    # log message
    logger.info(f"Request {uuid_id} completed in {time_elapsed:.2f}ms with status code {response.status_code}")

    # return response
    return response


def start_server():
    """This function starts a uvicorn server with a FastAPI instance.

    :raise: CodeChallengeInitializationError: If one or more environment variables were not set
    """

    # initialize logger
    log.initialize_app_logger(name=constants.APP_NAME)

    # load dotenv
    dotenv.load_dotenv()

    # check that the expected environment variables are provided
    check_env()

    # get port and host
    port, host = os.getenv(constants.ENV_PORT), os.getenv(constants.ENV_HOST)

    # register the main router with the module-level api instance
    main.register_router(api)

    # set up uvicorn
    uvicorn.run(app=api, port=port, host=host, debug=True)


if __name__ == "__main__":
    logging.warning(
        "Invoking the Code Challenge server module should only be done when debugging locally. Use the entry-point "
        "script to invoke this module from the command line in production."
    )
    start_server()
