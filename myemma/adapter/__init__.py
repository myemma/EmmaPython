import requests
from requests.auth import HTTPBasicAuth

class ApiRequestFailed(Exception): pass

class V1Adapter(object):
    """
    Emma APIv1 Adapter and Gateway
    """
    def __init__(self, auth):
        self.auth = HTTPBasicAuth(auth['public_key'], auth['private_key'])
        self.url = "https://api.e2ma.net/%s" % auth['account_id']

    def _process_response(self, response):
        if response.status_code == 404:
            return None
        elif response.status_code >= 400:
            raise ApiRequestFailed(response)

        return response.json

    def post(self, path, params):
        return self._process_response(
            requests.post(
                self.url + "%s" % path,
                params=params,
                auth=self.auth))

    def get(self, path, params):
        return self._process_response(
            requests.get(
                self.url + "%s" % path,
                params=params,
                auth=self.auth))

    def put(self, path, params):
        return self._process_response(
            requests.put(
                self.url + "%s" % path,
                params=params,
                auth=self.auth))

    def delete(self, path, params):
        return self._process_response(
            requests.delete(
                self.url + "%s" % path,
                params=params,
                auth=self.auth))

__all__ = ['V1Adapter']