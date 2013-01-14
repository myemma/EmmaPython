from base import BaseApiModel
from group import Group
from mailing import Mailing
from myemma.model.base import Collection

class NoMemberEmailError(Exception):
    """
    An API call was attempted with missing required parameters (email)
    """
    pass

class NoMemberIdError(Exception):
    """
    An API call was attempted with missing required parameters (id)
    """
    pass

class NoMemberStatusError(Exception):
    """
    An API call was attempted with missing required parameters (status)
    """
    pass


class Member(BaseApiModel):
    """
    Encapsulates operations for a :class:`Member`

    :param adapter: An HTTP client adapter from :mod:`myemma.adapter`
    :type adapter: :class:`object`
    :param raw: The raw values of this :class:`Member`
    :type raw: :class:`dict`
    """
    def __init__(self, adapter, raw = None):
        self.adapter = adapter
        self.groups = MemberGroupCollection(self.adapter, self)
        self.mailings = MemberMailingCollection(self.adapter, self)
        self._dict = raw if raw is not None else {}

    def opt_out(self):
        """
        Opt-out this :class:`Member` from future mailings on this :class:`Account`

        :rtype: :class:`None`
        """
        if not self._dict.has_key(u"email"):
            raise NoMemberEmailError()
        path = '/members/email/optout/%s' % self._dict[u"email"]
        if self.adapter.put(path):
            self._dict[u"status"] = u"opt-out"

    def get_opt_out_detail(self):
        """
        Get details about this :class:`Member`'s opt-out history

        :rtype: :class:`list`
        """
        if not self._dict.has_key(u"member_id"):
            raise NoMemberIdError()
        path = '/members/%s/optout' % self._dict[u"member_id"]
        return self.adapter.get(path)

    def has_opted_out(self):
        """
        Check if this :class:`Member` has opted-out

        :rtype: :class:`bool`
        """
        if not self._dict.has_key(u"status"):
            raise NoMemberStatusError()
        return self._dict[u"status"] == u"opt-out"


class MemberMailingCollection(Collection):
    """
    Encapsulates operations for the set of :class:`Mailing` objects of a :class:`Member`

    :param adapter: An HTTP client adapter from :mod:`myemma.adapter`
    :type adapter: :class:`object`
    :param member: The parent for this collection
    :type member: :class:`Member`
    """
    def __init__(self, adapter, member):
        self.member = member
        super(MemberMailingCollection, self).__init__(adapter)

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Mailing` objects

        :rtype: :class:`list` of :class:`Mailing` objects

        Usage::

            mem.mailings.fetch_all() # [Mailing, Mailing, ...]

        """
        if u"member_id" not in self.member:
            raise NoMemberIdError()
        path = '/members/%s/mailings' % self.member[u"member_id"]
        if not self._dict:
            self._dict = dict(map(
                lambda x: (x[u"mailing_id"], Mailing(self.adapter, x)),
                self.adapter.get(path)
            ))
        return self._dict

class MemberGroupCollection(Collection):
    """
    Encapsulates operations for the set of :class:`Group` objects of a :class:`Member`

    :param adapter: An HTTP client adapter from :mod:`myemma.adapter`
    :type adapter: :class:`object`
    :param member: The parent for this collection
    :type member: :class:`Member`
    """
    def __init__(self, adapter, member):
        self.member = member
        super(MemberGroupCollection, self).__init__(adapter)

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Group` objects

        :rtype: :class:`list` of :class:`Group` objects

        Usage::

            mem.groups.fetch_all() # [Group, Group, ...]

        """
        if u"member_id" not in self.member:
            raise NoMemberIdError()
        path = '/members/%s/groups' % self.member[u"member_id"]
        if not self._dict:
            self._dict = dict(map(
                lambda x: (x[u"group_name"], Group(self.adapter, x)),
                self.adapter.get(path)
            ))
        return self._dict

__all__ = ['Member', 'MemberGroupCollection', 'MemberMailingCollection',
           'NoMemberEmailError', 'NoMemberIdError', 'NoMemberStatusError']