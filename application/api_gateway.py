""" import packages """
import json
import logging
from flask import Flask, request, abort, make_response, jsonify, Response
from flask_restful import Resource, Api, reqparse
import config.config as config
import requests


class ApiGateway(Resource):
    """ApiGateway

    This class is used to forward the requests and return the response to the client

    methods:
        post()
        Listen for all the POST requests sent to this resource

        get()
        Listen for all the GET requests sent to this resource

        Missing to implement more http requests methods
    """
    logger = logging.getLogger(__name__)

    def post(self):
        #Forward the requests and return the response
        self.logger.debug("POST request")
        try:
            data = request.get_data()
            dictionary = {}

            tmp_url = request.args.get('url')
            if tmp_url == None:
                self.logger.error(
                    "The parameter [url] is required, sample: url=http://www.domain.com"
                )
                abort(
                    500,
                    "The parameter [url] is required, sample: url=http://www.domain.com"
                )
            #Get additional url parameters in case that exists to be sent in the request method
            url_args = request.args
            second_part = ""
            for url_arg in url_args:
                if url_arg != "url":
                    second_part = second_part + "&" + url_arg + "=" + request.args[
                        url_arg]

            tmp_url = tmp_url + second_part
            self.logger.info("Invoking the URL: [%s]", tmp_url)
            #Prepare headers to be sent as JSON in the request
            headers = request.headers
            for a, b in headers:
                dictionary.setdefault(a, b)

            headers = dictionary
            del headers['Host']

            x = requests.post(tmp_url, data=data, headers=headers)
            self.logger.debug("Request finished with status [%s]",
                              str(x.status_code))
            return make_response(x.text, x.status_code, x.headers.items())
        except Exception as err:
            self.logger.error(err)
            abort(500, str(err))

    def get(self):
        #Forward the requests and return the response
        self.logger.debug("GET request")
        dictionary = {}
        try:
            tmp_url = request.args.get('url')
            if tmp_url == None:
                self.logger.error(
                    "The parameter [url] is required, sample: url=http://www.domain.com"
                )
                abort(
                    500,
                    "The parameter [url] is required, sample: url=http://www.domain.com"
                )

            #Get additional url parameters in case that exists to be sent in the request method
            url_args = request.args
            second_part = ""
            for url_arg in url_args:
                if url_arg != "url":
                    second_part = second_part + "&" + url_arg + "=" + request.args[
                        url_arg]

            tmp_url = tmp_url + second_part
            self.logger.info("Invoking the URL: [%s]", tmp_url)
            #Prepare headers to be sent as JSON in the request
            headers = request.headers
            for a, b in headers:
                dictionary.setdefault(a, b)

            headers = dictionary
            del headers['Host']

            x = requests.get(tmp_url, headers=headers)
            self.logger.debug("Request finished with status [%s]",
                              str(x.status_code))
            return make_response(x.text, x.status_code, x.headers.items())
        except Exception as err:
            self.logger.error(err)
            abort(500, str(err))