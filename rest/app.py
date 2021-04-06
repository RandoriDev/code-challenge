"""Entry point of the application

This script is the entry point of the application and let's add the resources(Endpoints).

request_dict:  dict
    A global dict to keep the last request for all the clients, this is for this proof of concept, if we want the reproduce 
    this in production we need a separated cache, or a memory DB.

methods:
    log_request()
    Keeps the logic to intercept all the requests, also having the logic in this method means that if we add new resources we does not need 
    to reproduce the logic in the new endpoints.
"""
""" import packages """
import logging
from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_cors import CORS

from healthcheck import HealthCheck, EnvironmentDump
import config.config as config
import application.api_gateway as api_gateway
import application.dummy as dummy
import json
import time

LOGGER = logging.getLogger(__name__)
CONFIG = config.Config()

#Dict that contains the last requests with the IP as the key
#This could be better stored in redis or another key-> Value storage
request_dict = {}

if CONFIG.get_string("rest", "host") != "":
    HOST = CONFIG.get_string("rest", "host")
    LOGGER.info("Using host %s", HOST)
else:
    HOST = "0.0.0.0"
    LOGGER.info("Using default host %s", HOST)

if CONFIG.get_string("rest", "port") != "":
    PORT = CONFIG.get("rest", "port")
    LOGGER.info("Using port %s", str(PORT))
else:
    PORT = 3001
    LOGGER.info("Using default port %s", str(PORT))

if CONFIG.get("app", "debug") != "":
    DEBUG = CONFIG.get("app", "debug")
    LOGGER.info("Using debug %s", str(DEBUG))
else:
    DEBUG = True
    LOGGER.info("Using default debug %s", str(DEBUG))

APP = Flask(__name__)
cors = CORS(APP, resources={r"*": {"origins": "*"}})
api = Api(APP)

HEALTH = HealthCheck()
ENVDUMP = EnvironmentDump()

APP.add_url_rule("/randori/healthcheck",
                 "healthcheck",
                 view_func=lambda: HEALTH.run())

api.add_resource(api_gateway.ApiGateway, '/apiGateway')
api.add_resource(dummy.Dummy, '/dummy')


def run_rest_server():
    """ server """
    APP.run(host=HOST,
            port=PORT,
            debug=DEBUG,
            threaded=True,
            use_reloader=False)


@APP.before_request
def log_request():
    """Intercept all the requests and future requests, in this way the validations will be shared with all the implementing clasess """
    global request_dict

    if request.is_json:
        LOGGER.debug("Is JSON")
        tmp_json = request.get_json()
        #Actually looking into the root of the directory
        if "_malicious" in tmp_json:
            LOGGER.debug("Is a malicious request")
            abort(401)
    """Get the client IP, this to store the requests and know the requests is not the same """
    remote_addr = ""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        remote_addr = request.remote_addr
    else:
        remote_addr = request.environ['HTTP_X_FORWARDED_FOR']

    request_data = request.data

    dictionary = {}
    headers = request.headers
    for a, b in headers:
        dictionary.setdefault(a, b)

    headers = dictionary
    user_agent = request.user_agent.__str__().strip()
    #Comparing the last requests to see if two requests in a row are the same
    if remote_addr in request_dict:
        #Compare the requests headers
        same_headers = True
        request_headers = request_dict[remote_addr]["headers"]
        for key in headers.keys():
            if key in request_headers:
                headerValue = headers[key]
                requestHeaderValue = request_headers[key]
                if headerValue.__str__() != requestHeaderValue.__str__():
                    same_headers = False
                    break
        #Compare the request Body
        same_body = False
        if request_data == request_dict[remote_addr]["request_data"]:
            same_body = True

        #Compare the user-agent
        same_user_agent = False
        if user_agent == request_dict[remote_addr]["user_agent"]:
            same_user_agent = True
        LOGGER.debug("same_user_agent[%s]", same_user_agent)
        LOGGER.debug("same_body[%s]", same_body)
        LOGGER.debug("same_headers[%s]", same_headers)
        if same_headers and same_body and same_user_agent:
            LOGGER.debug("Same requests in a row")
            #Sleep two seconds
            time.sleep(2)

    request_dict[remote_addr] = {
        "headers": headers,
        "request_data": request_data,
        "user_agent": user_agent
    }
    #LOGGER.debug("Request Headers %s", requestDict)
    return None


if __name__ == '__main__':
    run_rest_server()
