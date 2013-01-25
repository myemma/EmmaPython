"""
Provides a place to put any layer of abstraction between this wrapper and a
needed HTTP client library
"""


class AbstractAdapter(object):
    """
    Abstract Adapter
    """
    MAX_PAGE_SIZE = 500

    def __init__(self):
        self.count_only = False
        self.start = 0
        self.end = self.__class__.MAX_PAGE_SIZE

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

    def pagination_add_ons(self):
        if self.count_only:
            return {'count': True}

        if self.start != 0 or self.end != self.__class__.MAX_PAGE_SIZE:
            return {
                'start': self.start,
                'end': self.end
            }

        return {}
