"""Audience webhook models"""

from datetime import datetime
from myemma import exceptions as ex
from myemma.model import BaseApiModel, str_fields_to_datetime


class WebHook(BaseApiModel):
    """
    Encapsulates operations for a :class:`WebHook`

    :param account: The Account which owns this WebHook
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`WebHook`
    :type raw: :class:`dict`

    Usage::

        >>> from myemma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> acct.webhooks[123]
        <WebHook>
    """
    def __init__(self, account, raw=None):
        self.account = account
        super(WebHook, self).__init__(raw)

    def delete(self):
        """
        Delete this webhook

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> wbhk = acct.webhooks[123]
            >>> wbhk.delete()
            None
        """
        if not 'webhook_id' in self._dict:
            raise ex.NoWebHookIdError()

        path = "/webhooks/%s" % self._dict['webhook_id']
        self.account.adapter.delete(path)
        if self._dict['webhook_id'] in self.account.webhooks:
            del(self.account.webhooks._dict[self._dict['webhook_id']])

    def extract(self):
        """
        Extracts data from the model in a format suitable for using with the API

        :rtype: :class:`dict`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> wbhk = acct.webhooks[123]
            >>> wbhk.extract()
            {'name':..., 'criteria':...}
        """
        keys = ['url', 'event', 'method', 'public_key']

        return dict(x for x in self._dict.items() if x[0] in keys)

    def _add(self):
        """Add a single trigger"""
        path = '/webhooks'
        data = self.extract()
        self._dict['webhook_id'] = self.account.adapter.post(path, data)
        self.account.triggers._dict[self._dict['webhook_id']] = self

    def _update(self):
        """Update a single trigger"""
        path = '/webhooks/%s' % self._dict['webhook_id']
        data = self.extract()
        self.account.adapter.put(path, data)

    def save(self):
        """
        Add or update this :class:`WebHook`

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> wbhk = acct.webhooks[123]
            >>> wbhk['url'] = u"http://v2.example.com"
            >>> wbhk.save()
            123
            >>> from myemma.enumerations import WebHookMethod
            >>> wbhk = acct.webhooks.factory(
            ...     {
            ...         'event': u"mailing_finish",
            ...         'url': u"http://example.com",
            ...         'method': WebHookMethod.Get
            ...     }
            ... )
            >>> wbhk.save()
            124
        """
        if 'webhook_id' not in self._dict:
            return self._add()
        else:
            return self._update()
