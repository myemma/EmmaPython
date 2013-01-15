from . import (BaseApiModel, Collection, NoMemberEmailError, NoMemberIdError,
               NoMemberStatusError)
from group import Group
from mailing import Mailing


class Member(BaseApiModel):
    """
    Encapsulates operations for a :class:`Member`

    :param adapter: An HTTP client adapter from :mod:`myemma.adapter`
    :type adapter: :class:`AbstractAdapter`
    :param raw: The raw values of this :class:`Member`
    :type raw: :class:`dict`

    Usage::

        >>> mbr = acct.members.factory()
        >>> mbr
        <Member>
        >>> mbr.groups
        <MemberGroupCollection>
        >>> mbr.mailings
        <MemberMailingCollection>
    """
    def __init__(self, account, raw = None):
        self.account = account
        self.groups = MemberGroupCollection(self)
        self.mailings = MemberMailingCollection(self)
        self._dict = raw if raw is not None else {}

    def opt_out(self):
        """
        Opt-out this :class:`Member` from future mailings on this
        :class:`Account`

        :rtype: :class:`None`

        Usage::

            >>> mbr.opt_out()
            None
        """
        if u"email" not in self._dict:
            raise NoMemberEmailError()
        path = '/members/email/optout/%s' % self._dict[u"email"]
        if self.account.adapter.put(path):
            self._dict[u"status"] = u"opt-out"

    def get_opt_out_detail(self):
        """
        Get details about this :class:`Member`'s opt-out history

        :rtype: :class:`list`

        Usage::

            >>> mbr.get_opt_out_detail()
            [...]
        """
        if u"member_id" not in self._dict:
            raise NoMemberIdError()
        path = '/members/%s/optout' % self._dict[u"member_id"]
        return self.account.adapter.get(path)

    def has_opted_out(self):
        """
        Check if this :class:`Member` has opted-out

        :rtype: :class:`bool`

        Usage::

            >>> mbr.has_opted_out()
            False
        """
        if u"status" not in self._dict:
            raise NoMemberStatusError()
        return self._dict[u"status"] == u"opt-out"

    def extract(self, top_level=None):
        """
        Extracts data from the model in a format suitable for using with the API

        ;param top_level: Set of top-level attributes of the resulting JSON
        object. All other attributes will be treated as member fields.
        :type top_level: :class:`list` of :class:`str` or :class:`None`
        :rtype: :class:`dict`

        Usage::

            >>> mbr.extract()
            {'member_id':123, 'email':u"test@example.org", 'fields':{...}}
        """
        if 'email' not in self._dict:
            raise NoMemberEmailError

        # Set some defaults
        if top_level is None:
            top_level = ['member_id', 'email']

        def squash(d, t):
            #squash a member tuple into member dictionary
            if t[0] in top_level:
                d[t[0]] = t[1]
            else:
                if 'fields' not in d:
                    d['fields'] = {}
                d['fields'][t[0]] = t[1]
            return d

        shortcuts = self.account.fields.export_shortcuts()

        return dict(
            reduce(
                lambda x, y: squash(x, y),
                filter(
                    lambda x: x[0] in shortcuts + top_level,
                    self._dict.items()),
                {}))


class MemberMailingCollection(Collection):
    """
    Encapsulates operations for the set of :class:`Mailing` objects of a
    :class:`Member`

    :param adapter: An HTTP client adapter from :mod:`myemma.adapter`
    :type adapter: :class:`AbstractAdapter`
    :param member: The parent for this collection
    :type member: :class:`Member`
    """
    def __init__(self, member):
        self.member = member
        super(MemberMailingCollection, self).__init__(member.account.adapter)

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Mailing` objects

        :rtype: :class:`list` of :class:`Mailing` objects

        Usage::

            >>> mbr.mailings.fetch_all()
            [<Mailing>, <Mailing>, ...]

        """
        if u"member_id" not in self.member:
            raise NoMemberIdError()
        path = '/members/%s/mailings' % self.member[u"member_id"]
        if not self._dict:
            self._dict = dict(map(
                lambda x: (x[u"mailing_id"], Mailing(self.member.account, x)),
                self.member.account.adapter.get(path)
            ))
        return self._dict


class MemberGroupCollection(Collection):
    """
    Encapsulates operations for the set of :class:`Group` objects of a
    :class:`Member`

    :param adapter: An HTTP client adapter from :mod:`myemma.adapter`
    :type adapter: :class:`AbstractAdapter`
    :param member: The parent for this collection
    :type member: :class:`Member`
    """
    def __init__(self, member):
        self.member = member
        super(MemberGroupCollection, self).__init__(self.member.account.adapter)

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Group` objects

        :rtype: :class:`list` of :class:`Group` objects

        Usage::

            >>> mbr.groups.fetch_all()
            [<Group>, <Group>, ...]

        """
        if u"member_id" not in self.member:
            raise NoMemberIdError()
        path = '/members/%s/groups' % self.member[u"member_id"]
        if not self._dict:
            self._dict = dict(map(
                lambda x: (x[u"group_name"], Group(self.member.account, x)),
                self.member.account.adapter.get(path)
            ))
        return self._dict
