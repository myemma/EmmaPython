"""
Provides a place to put any layer of abstraction between this wrapper and a
needed HTTP client library
"""


class AbstractAdapter(object):
    """
    Abstract Adapter
    """
    def post(self, path, params=None):
        """HTTP POST"""
        pass

    def get(self, path, params=None):
        """HTTP GET"""
        pass

    def put(self, path, params=None):
        """HTTP PUT"""
        pass

    def delete(self, path, params=None):
        """HTTP DELETE"""
        pass
