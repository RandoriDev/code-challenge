from flask import Flask, request, abort, Response, jsonify
from httpservice.service.backend import process_request_backend
from httpservice.app.validation import is_malicious, repeat_request
import json
import time
import urllib
import logging
import requests
import asyncio

# URL to contact the backend service
backend = "http://127.0.0.1:5001"

app = Flask('Code Challenge Server')
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
LOG = app.logger

@app.route('/', methods=['POST'])
def home() -> Response:

    LOG.info('{} method called'.format(__name__))
    content = request.get_json(force=True)

    # load the request json
    payload = json.dumps(content)
    
    errors = is_malicious(request)
    if errors is not None:
        LOG.error('Malicious request received')
        # A better way of throwing 401 errors is using the InvalidUsage exception
        abort(401)

    if (repeat_request(ip=request.remote_addr, payload=payload.encode('utf-8'))):
        LOG.info('Sleeping for 2 seconds')
        time.sleep(2)

    #backend micro service implementation
    r = call_backend_service(request)
    headers = dict(r.raw.headers)
    def generate():
        for chunk in r.raw.stream(decode_content=False):
            yield chunk
    out = Response(generate(), headers=headers)
    out.status_code = r.status_code
    return out

def call_backend_service(request):
    """ Call the backend microservice

        Parameters
        ----------
        request : flask.request
            The unaltered request received from the client

    """
    LOG.info("Call backend service")
    return requests.request('GET', backend, params=request.args, stream=True, headers=dict(request.headers), data=request.form)

if __name__ == '__main__':
   app.run(port=80)