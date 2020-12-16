import os
import time
from functools import wraps

import flask
from flask import (
    jsonify, request, make_response
)

RATE_LIMITED_COOKIE = "rate_limited"
RATE_LIMITED_PAUSE_SECONDS: int = int(os.getenv("RATE_LIMITED_PAUSE_SECONDS", default=2))
RATE_LIMITED_AGE_SECONDS: int = int(os.getenv("RATE_LIMITED_AGE_SECONDS", default=5))


def reject_malicious_payload(f):
    """
    If the request is a POST with a json body that contains the key ‘is_malicious’ with the value then don’t
    forward the request and return a HTTP 401 to the client.
    """

    @wraps(f)
    def wrapped(*args, **kw):
        json = request.get_json()
        if json and "is_malicious" in json and request.method == 'POST':
            return jsonify({"error": "JSON body contained token is_malicious", "json": json}), 401, {'ContentType': 'application/json'}
        else:
            return f(*args, **kw)
    return wrapped


def rate_limited(f):
    """
    If the same client makes the exact same request twice
    in a row wait 2 seconds before passing the request to the backend.
    """
    def decorated_function(*args, **kws):
        response = f(*args, **kws)
        response = make_response(response)
        if RATE_LIMITED_COOKIE in flask.request.cookies.keys():
            time.sleep(RATE_LIMITED_PAUSE_SECONDS)
        response.set_cookie(RATE_LIMITED_COOKIE, max_age=RATE_LIMITED_AGE_SECONDS)
        return response
    return decorated_function
