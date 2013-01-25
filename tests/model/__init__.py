from emma.adapter import AbstractAdapter

class MockAdapter(AbstractAdapter):
    expected = None
    raised = None

    def __init__(self, *args, **kwargs):
        super(MockAdapter, self).__init__()
        self.called = 0
        self.call = ()

    def _capture(self, method, path, params):
        self.called += 1
        self.call = (method, path, params)

    def get(self, path, params=None):
        self._capture('GET', path, params if params else {})
        if self.__class__.raised:
            raise self.__class__.raised
        return self.__class__.expected

    def post(self, path, data=None):
        self._capture('POST', path, data if data else {})
        if self.__class__.raised:
            raise self.__class__.raised
        return self.__class__.expected

    def put(self, path, data=None):
        self._capture('PUT', path, data if data else {})
        if self.__class__.raised:
            raise self.__class__.raised
        return self.__class__.expected

    def delete(self, path, params=None):
        self._capture('DELETE', path, params if params else {})
        if self.__class__.raised:
            raise self.__class__.raised
        return self.__class__.expected