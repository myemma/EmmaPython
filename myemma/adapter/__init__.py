"""
Provides a place to put any layer of abstraction between this wrapper and a
needed HTTP client library
"""

class ApiRequestFailed(Exception):
    """
    Denotes a failure interacting with the API, such as HTTP 401 Unauthorized
    """
    pass


class AbstractAdapter(object):
    """
    Abstract Adapter
    """

    def post(self, path, params={}):
        raise NotImplementedError()

    def get(self, path, params={}):
        raise NotImplementedError()

    def put(self, path, params={}):
        raise NotImplementedError()

    def delete(self, path, params={}):
        raise NotImplementedError()
