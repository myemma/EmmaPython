"""Adapter for the Requests Library"""

import json
import requests
import requests.auth
from emma import exceptions as ex
from emma.adapter import AbstractAdapter


def process_response(response):
    """Takes a :class:`Response` and produces python built-ins"""
    if response.status_code == 400:
        raise ex.ApiRequest400(response)
    elif response.status_code == 404:
        return None
    elif response.status_code > 200:
        raise ex.ApiRequestFailed(response)

    return response.json()


class RequestsAdapter(AbstractAdapter):
    """
    Emma API Adapter for the `Requests Library
    <http://docs.python-requests.org/>`_

    :param auth: A dictionary with keys for your account id and public/private
                 keys
    :type auth: :class:`dict`

    Usage::

        >>> from emma.adapter.requests_adapter import RequestsAdapter
        >>> adptr = RequestsAdapter({
        ...     "account_id": "1234",
        ...     "public_key": "08192a3b4c5d6e7f",
        ...     "private_key": "f7e6d5c4b3a29180"})
        >>> adptr
        <RequestsAdapter>

    """
    def __init__(self, auth):
        super(RequestsAdapter, self).__init__()
        self.auth = requests.auth.HTTPBasicAuth(
            auth['public_key'],
            auth['private_key'])
        self.url = "https://api.e2ma.net/%s" % auth['account_id']

    def post(self, path, data=None):
        """
        Takes an effective path (portion after https://api.e2ma.net/:account_id)
        and a parameter dictionary, then passes these to :func:`requests.post`

        :param path: The path portion of a URL
        :type path: :class:`str`
        :param data: The content to encode
        :type data: :class:`object`
        :rtype: JSON-encoded value or None (if 404)

        Usage::

            >>> from emma.adapter.requests_adapter import RequestsAdapter
            >>> adptr = RequestsAdapter({
            ...     "account_id": "1234",
            ...     "public_key": "08192a3b4c5d6e7f",
            ...     "private_key": "f7e6d5c4b3a29180"})
            >>> adptr.post('/members', {...})
            {'import_id': 2001}
        """
        return process_response(
            requests.post(
                self.url + "%s" % path,
                data=json.dumps(data),
                auth=self.auth))

    def get(self, path, params=None):
        """
        Takes an effective path (portion after https://api.e2ma.net/:account_id)
        and a parameter dictionary, then passes these to :func:`requests.get`

        :param path: The path portion of a URL
        :type path: :class:`str`
        :param params: The dictionary of HTTP parameters to encode
        :type params: :class:`dict`
        :rtype: JSON-encoded value or None (if 404)

        Usage::

            >>> from emma.adapter.requests_adapter import RequestsAdapter
            >>> adptr = RequestsAdapter({
            ...     "account_id": "1234",
            ...     "public_key": "08192a3b4c5d6e7f",
            ...     "private_key": "f7e6d5c4b3a29180"})
            >>> adptr.get('/members', {...})
            [{...}, {...}, ...] # first 500 only
            >>> adptr.count_only = True
            >>> adptr.get('/members', {...})
            999
            >>> adptr.start = 500
            >>> adptr.end = 1000
            >>> adptr.get('/members', {...})
            [{...}, {...}, ...] # 500-999
        """

        params = params or {}
        params.update(self.pagination_add_ons())

        return process_response(
            requests.get(
                self.url + "%s" % path,
                params=params,
                auth=self.auth))

    def put(self, path, data=None):
        """
        Takes an effective path (portion after https://api.e2ma.net/:account_id)
        and a parameter dictionary, then passes these to :func:`requests.put`

        :param path: The path portion of a URL
        :type path: :class:`str`
        :param data: The content to encode
        :type data: :class:`object`
        :rtype: JSON-encoded value or None (if 404)

        Usage::

            >>> from emma.adapter.requests_adapter import RequestsAdapter
            >>> adptr = RequestsAdapter({
            ...     "account_id": "1234",
            ...     "public_key": "08192a3b4c5d6e7f",
            ...     "private_key": "f7e6d5c4b3a29180"})
            >>> adptr.put('/members/email/optout/test@example.com')
            True
        """
        return process_response(
            requests.put(
                self.url + "%s" % path,
                data=json.dumps(data),
                auth=self.auth))

    def delete(self, path, params=None):
        """
        Takes an effective path (portion after https://api.e2ma.net/:account_id)
        and a parameter dictionary, then passes these to :func:`requests.delete`

        :param path: The path portion of a URL
        :type path: :class:`str`
        :param params: The dictionary of HTTP parameters to encode
        :type params: :class:`dict`
        :rtype: JSON-encoded value or None (if 404)

        Usage::

            >>> from emma.adapter.requests_adapter import RequestsAdapter
            >>> adptr = RequestsAdapter({
            ...     "account_id": "1234",
            ...     "public_key": "08192a3b4c5d6e7f",
            ...     "private_key": "f7e6d5c4b3a29180"})
            >>> adptr.delete('/members/123')
            True
        """
        return process_response(
            requests.delete(
                self.url + "%s" % path,
                params=params,
                auth=self.auth))
