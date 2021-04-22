"""
Randori Code Challenge responder server module that can be used to test the main server.
"""

import logging
import os

import dotenv
import fastapi
import uvicorn

from code_challenge import constants, log
from code_challenge.routers import backend
from code_challenge.server import CodeChallengeInitializationError


def check_env():
    """This function checks that specific environment variables have been provided.

    :raise: CodeChallengeInitializationError: If one or more environment variables were not set
    """

    errors = []

    if not os.getenv(constants.ENV_BACKEND_HOST):
        errors.append(f"{constants.ENV_BACKEND_HOST} must be provided as an environment variable")

    if not os.getenv(constants.ENV_BACKEND_PORT):
        errors.append(f"{constants.ENV_BACKEND_PORT} must be provided as an environment variable")

    if errors:
        logger = logging.getLogger(constants.BACKEND_APP_NAME)
        for error in errors:
            logger.error(error)

        raise CodeChallengeInitializationError(
            "Backend server could not start due to startup errors. See event log for more detail."
        )


def create_api() -> fastapi.FastAPI:
    """This function creates an API instance.

    :return: FastAPI instance
    """

    # create an API instance
    api = fastapi.FastAPI()

    # register the backend router with the api instance
    backend.register_router(api)

    return api


def start_server():
    """This function starts a uvicorn server with a FastAPI instance.

    :raise: CodeChallengeInitializationError: If one or more environment variables were not set
    """

    # initialize logger
    log.initialize_app_logger(name=constants.BACKEND_APP_NAME)

    # load dotenv
    dotenv.load_dotenv()

    # check that the expected environment variables are provided
    check_env()

    # get port and host
    port, host = os.getenv(constants.ENV_BACKEND_PORT), os.getenv(constants.ENV_BACKEND_HOST)

    # create the API
    api = create_api()

    # set up uvicorn
    uvicorn.run(app=api, port=port, host=host)


if __name__ == "__main__":
    logging.warning(
        "Invoking the Code Challenge backend server module should only be done when debugging locally. Use the "
        "entry-point script to invoke this module from the command line in production."
    )
    start_server()
