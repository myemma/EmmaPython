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

        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> mbr = acct.members[123]
        >>> mbr
        <Member>
        >>> mbr.groups
        <MemberGroupCollection>
        >>> mbr.mailings
        <MemberMailingCollection>
    """
    def __init__(self, account, raw=None):
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

            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.opt_out()
            None
        """
        if 'email' not in self._dict:
            raise NoMemberEmailError()
        path = '/members/email/optout/%s' % self._dict['email']
        if self.account.adapter.put(path):
            self._dict['status'] = u"opt-out"

    def get_opt_out_detail(self):
        """
        Get details about this :class:`Member`'s opt-out history

        :rtype: :class:`list`

        Usage::

            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.get_opt_out_detail()
            [...]
        """
        if 'member_id' not in self._dict:
            raise NoMemberIdError()
        path = '/members/%s/optout' % self._dict['member_id']
        return self.account.adapter.get(path)

    def has_opted_out(self):
        """
        Check if this :class:`Member` has opted-out

        :rtype: :class:`bool`

        Usage::

            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.has_opted_out()
            False
            >>> mbr.opt_out()
            >>> mbr.has_opted_out()
            True
        """
        if 'status' not in self._dict:
            raise NoMemberStatusError()
        return self._dict['status'] == u"opt-out"

    def extract(self, top_level=None):
        """
        Extracts data from the model in a format suitable for using with the API

        ;param top_level: Set of top-level attributes of the resulting JSON
        object. All other attributes will be treated as member fields.
        :type top_level: :class:`list` of :class:`str` or :class:`None`
        :rtype: :class:`dict`

        Usage::

            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
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

    def save(self, signup_form_id=None):
        """
        Add or update this :class:`Member`

        :rtype: :class:`None`

        Usage::

            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr['last_name'] = u"New-Name"
            >>> mbr.save()
            None
            >>> mbr = acct.members.factory({'email': u"new@example.com"})
            >>> mbr.save()
            None
        """
        path = '/members/add'
        data = self.extract()
        if len(self.groups):
            data['group_ids'] = self.groups.fetch_all().keys()
        if signup_form_id:
            data['signup_form_id'] = signup_form_id

        outcome = self.account.adapter.post(path, data)
        self['status_code'] = outcome['status']
        if outcome['added']:
            self['member_id'] = outcome['member_id']


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

        :rtype: :class:`dict` of :class:`Mailing` objects

        Usage::

            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.mailings.fetch_all()
            {123: <Mailing>, 321: <Mailing>, ...}

        """
        if 'member_id' not in self.member:
            raise NoMemberIdError()
        path = '/members/%s/mailings' % self.member['member_id']
        if not self._dict:
            self._dict = dict(map(
                lambda x: (x['mailing_id'], Mailing(self.member.account, x)),
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

        :rtype: :class:`dict` of :class:`Group` objects

        Usage::

            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.groups.fetch_all()
            {123: <Group>, 321: <Group>, ...}

        """
        if 'member_id' not in self.member:
            raise NoMemberIdError()
        path = '/members/%s/groups' % self.member['member_id']
        if not self._dict:
            self._dict = dict(map(
                lambda x: (x['group_name'], Group(self.member.account, x)),
                self.member.account.adapter.get(path)
            ))
        return self._dict
