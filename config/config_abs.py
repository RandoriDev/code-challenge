""" import packages """
from abc import ABC, abstractmethod


class ConfigAbs(ABC):
    """ class ConfigAbs """
    @abstractmethod
    def get_string(self, *args):
        """ get_string """
        raise NotImplementedError

    @abstractmethod
    def get(self, *args):
        """ get """
        raise NotImplementedError
