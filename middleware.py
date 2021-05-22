#!/usr/bin/env python3

import logging
import socket
import http.server
import time
import json
import requests

MIN_TIMEOUT_TIME = 2000
SERVER_PORT = 8000
ACCESS_CACHE = {}
BACKEND_ENDPOINT = "https://example.com"

logging.basicConfig(
    format='%(asctime)s %(message)s',
    filename='middleware.log',
    encoding='utf-8',
    level=logging.DEBUG
)

def inspect_request_frequency():
    """
    inspect_request_frequency() -> void

    Function checks if the exact same request was twice in a row
    and waits 2 seconds before passing the request to the backend.
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    current_time = round(time.time() * 1000)
    logging.debug("ip_address = {0}, current_time = {1}".format(ip_address, current_time))

    if ip_address in ACCESS_CACHE.keys():
        last_time = ACCESS_CACHE[ip_address]
        actual_timeout = current_time - last_time
        logging.debug("last_time = {0}, actual_timeout = {1}".format(last_time, actual_timeout))

        if MIN_TIMEOUT_TIME > actual_timeout:
            required_timeout = (MIN_TIMEOUT_TIME - actual_timeout) / 1000
            logging.info("client waits for required timeout = {0}...".format(required_timeout))
            time.sleep(required_timeout)

    ACCESS_CACHE[ip_address] = current_time
    logging.info("updated cache object = {0}".format(str(ACCESS_CACHE)))


def request_backend(method='get', json_data={}):
    """
    inspect_request_frequency(method,json_data) -> object

    Request forwarded unaltered and the backend’s response returns to the client.
    """
    logging.info("requesting backend service; method = {0}, json_data = {1}".format(method, json_data))
    if method == 'get':
        response = requests.get(BACKEND_ENDPOINT)
    else:
        response = requests.post(BACKEND_ENDPOINT, json=json_data)

    return response


class HttpRequestHandlerClass(http.server.BaseHTTPRequestHandler):
    """ Wrapper for HTTP request handler base class."""
    def do_GET(self):
        inspect_request_frequency()
        backend_response = request_backend()
        logging.debug("backend headers = {0}, content = {1}".
                      format(str(backend_response.headers), str(backend_response.content)))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(backend_response.content)

    def do_POST(self):
        inspect_request_frequency()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data.decode('utf-8')) if len(post_data) else {}
        logging.debug("request path = {0}, json_data = {1}".format(str(self.path), str(post_data)))

        if "is_malicious" in json_data.keys():
            # don't forward the request and return a HTTP 401 to the client
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        else:
            # pass the request to the backend
            backend_response = request_backend(method='post', json_data=json_data)
            logging.debug("backend headers = {0}, content = {1}".
                          format(str(backend_response.headers), str(backend_response.content)))

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(backend_response.content)


def start_http_server():
    """
    start_http_server-> void

    Spawns local web server.
    """
    logging.info("spawning http server at port {0}...".format(SERVER_PORT))
    with http.server.HTTPServer(('', SERVER_PORT), HttpRequestHandlerClass) as server:
        server.serve_forever()
        logging.info("http server at port {0} spawned".format(SERVER_PORT))


if __name__ == '__main__':
    start_http_server()
