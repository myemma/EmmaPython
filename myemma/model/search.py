"""Audience search models"""

from datetime import datetime
from myemma import exceptions as ex
from myemma.model import BaseApiModel, str_fields_to_datetime


class Search(BaseApiModel):
    """
    Encapsulates operations for a :class:`Search`

    :param account: The Account which owns this Search
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Search`
    :type raw: :class:`dict`

    Usage::

        >>> from myemma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> srch = acct.searches[123]
        >>> srch
        <Search>
    """
    def __init__(self, account, raw=None):
        self.account = account
        super(Search, self).__init__(raw)

    def _parse_raw(self, raw):
        raw.update(str_fields_to_datetime(['deleted_at', 'last_run_at'], raw))
        return raw

    def is_deleted(self):
        """
        Whether a search has been deleted

        :rtype: :class:`bool`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> srch = acct.searches[123]
            >>> srch.is_deleted()
            False
            >>> srch.delete()
            >>> srch.is_deleted()
            True
        """
        return 'deleted_at' in self._dict and bool(self._dict['deleted_at'])

    def delete(self):
        """
        Delete this search

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> srch = acct.searches[123]
            >>> srch.delete()
            None
        """
        if not 'search_id' in self._dict:
            raise ex.NoSearchIdError()
        if self.is_deleted():
            return None

        path = "/searches/%s" % self._dict['search_id']
        if self.account.adapter.delete(path):
            self._dict['deleted_at'] = datetime.now()
        if self._dict['search_id'] in self.account.searches:
            del(self.account.searches._dict[self._dict['search_id']])
