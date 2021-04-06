""" import packages """
import json
import logging
from flask import Flask, request, abort, make_response, jsonify, Response
from flask_restful import Resource, Api, reqparse
import config.config as config
import requests


class Dummy(Resource):
    """Dummy

    This class is used to test the forward functionality
    """
    logger = logging.getLogger(__name__)

    def post(self):
        #Dummy response
        self.logger.debug("POST request")
        try:
            data = {"Test1": "Dummy POST"}

            return data
        except Exception as err:
            self.logger.error(err)
            abort(500, str(err))

    def get(self):
        #Dummy response
        self.logger.debug("GET request")
        try:
            data = {"Test1": "Dummy GET"}

            return data
        except Exception as err:
            self.logger.error(err)
            abort(500, str(err))