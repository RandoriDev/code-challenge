""" import packages """
import json
import logging.config
import os
import yaml

import config.config_abs as config_abs


class Config(config_abs.ConfigAbs):
    """ class Config """
    def __init__(self):
        super().__init__()
        config_filename = 'config/config.json'
        if 'CONFIG_FILE' in os.environ:
            config_filename = os.environ["CONFIG_FILE"]

        with open(config_filename) as v_file:
            self.config = json.loads(v_file.read())

        logging_config_file = 'config/logging.yml'
        if 'LOGGING_CONFIG_FILE' in os.environ:
            logging_config_file = os.environ["LOGGING_CONFIG_FILE"]

        with open(logging_config_file) as v_file:
            v_d = yaml.load(v_file)
            v_d.setdefault('version', 1)
            logging.config.dictConfig(v_d)

    def get_string(self, *args):
        v_value = self.config
        for arg in args:
            # print("arg: "+ arg)
            #if type(v_value) is dict and arg in v_value:
            if isinstance(v_value, dict) and arg in v_value:
                v_value = v_value[arg]
            else:
                return ""
        v_res = ""
        if isinstance(v_value, str):
            v_res = v_value
        return v_res

    def get(self, *args):
        v_value = self.config
        for arg in args:
            if isinstance(v_value, dict) and arg in v_value:
                v_value = v_value[arg]
            else:
                return ""
        return v_value
