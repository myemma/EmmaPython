"""Audience search models"""

from datetime import datetime
from emma import exceptions as ex
from emma.model import BaseApiModel, str_fields_to_datetime
import emma.model.member


class Search(BaseApiModel):
    """
    Encapsulates operations for a :class:`Search`

    :param account: The Account which owns this Search
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Search`
    :type raw: :class:`dict`

    Usage::

        >>> from emma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> srch = acct.searches[123]
        >>> srch
        <Search>
    """
    def __init__(self, account, raw=None):
        self.account = account
        super(Search, self).__init__(raw)
        self.members = SearchMemberCollection(self)

    def _parse_raw(self, raw):
        raw.update(str_fields_to_datetime(['deleted_at', 'last_run_at'], raw))
        return raw

    def is_deleted(self):
        """
        Whether a search has been deleted

        :rtype: :class:`bool`

        Usage::

            >>> from emma.model.account import Account
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

            >>> from emma.model.account import Account
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

    def extract(self):
        """
        Extracts data from the model in a format suitable for using with the API

        :rtype: :class:`dict`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> srch = acct.searches[123]
            >>> srch.extract()
            {'name':..., 'criteria':...}
        """
        keys = ['name', 'criteria']

        return dict(x for x in self._dict.items() if x[0] in keys)

    def _add(self):
        """Add a single search"""
        path = '/searches'
        data = self.extract()
        self._dict['search_id'] = self.account.adapter.post(path, data)
        self.account.searches._dict[self._dict['search_id']] = self

    def _update(self):
        """Update a single search"""
        path = '/searches/%s' % self._dict['search_id']
        data = self.extract()
        self.account.adapter.put(path, data)

    def save(self):
        """
        Add or update this :class:`Search`

        :rtype: :class:`None`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> srch = acct.searches[123]
            >>> srch['name'] = u"Renamed Search"
            >>> srch.save()
            123
            >>> srch = acct.searches.factory(
            ...     {
            ...         'name': u"Test Search",
            ...         'criteria': ["group", "eq", "Test Group"]
            ...     }
            ... )
            >>> srch.save()
            124
        """
        if 'search_id' not in self._dict:
            return self._add()
        else:
            return self._update()


class SearchMemberCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Member` objects of a
    :class:`Search`

    :param search: The search which owns this collection
    :type search: :class:`Search`
    """
    def __init__(self, search):
        self.search = search
        super(SearchMemberCollection, self).__init__()

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Member` objects

        :rtype: :class:`dict` of :class:`Member` objects

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> srch = acct.searches[1024]
            >>> srch.members.fetch_all()
            {200: <Member>, 201: <Member>, ...}
        """
        if not 'search_id' in self.search:
            raise ex.NoSearchIdError()

        path = '/searches/%s/members' % self.search['search_id']
        if not self._dict:
            member = emma.model.member
            self._dict = dict(
                (x['member_id'], member.Member(self.search.account, x))
                    for x in self.search.account.adapter.paginated_get(path))
        return self._dict
