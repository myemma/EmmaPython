from . import (BaseApiModel, ModelWithDateFields, NoMemberEmailError,
               NoMemberIdError, NoMemberStatusError, MemberUpdateError)
from group import Group
from mailing import Mailing
import member_status


class Member(BaseApiModel, ModelWithDateFields):
    """
    Encapsulates operations for a :class:`Member`

    :param account: The Account which owns this Member
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Member`
    :type raw: :class:`dict`

    Usage::

        >>> from myemma.model.account import Account
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
        super(Member, self).__init__(raw)

    def _parse_raw(self, raw):
        if 'status' in raw:
            raw['status'] = member_status.MemberStatus.factory(raw['status'])
        if 'member_status_id' in raw:
            del(raw['member_status_id'])
        if 'fields' in raw:
            raw.update(raw['fields'])
            del(raw['fields'])
        self._str_fields_to_datetime(
            ['last_modified_at', 'member_since', 'deleted_at'],
            raw)
        return raw

    def opt_out(self):
        """
        Opt-out this :class:`Member` from future mailings on this
        :class:`Account`

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.opt_out()
            None
        """
        if 'email' not in self._dict:
            raise NoMemberEmailError()
        path = '/members/email/optout/%s' % self._dict['email']
        if self.account.adapter.put(path):
            self._dict['status'] = member_status.OptOut

    def get_opt_out_detail(self):
        """
        Get details about this :class:`Member`'s opt-out history

        :rtype: :class:`list`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.get_opt_out_detail()
            [...]
        """
        if 'member_id' not in self._dict:
            raise NoMemberIdError()
        if self._dict['status'] != member_status.OptOut:
            return []

        path = '/members/%s/optout' % self._dict['member_id']
        return self.account.adapter.get(path)

    def has_opted_out(self):
        """
        Check if this :class:`Member` has opted-out

        :rtype: :class:`bool`

        Usage::

            >>> from myemma.model.account import Account
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
        print(repr(self._dict['status']))
        return self._dict['status'] == member_status.OptOut

    def extract(self, top_level=None):
        """
        Extracts data from the model in a format suitable for using with the API

        :param top_level: Set of top-level attributes of the resulting JSON
        object. All other attributes will be treated as member fields.
        :type top_level: :class:`list` of :class:`str` or :class:`None`
        :rtype: :class:`dict`

        Usage::

            >>> from myemma.model.account import Account
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

    def _add(self, signup_form_id):
        path = '/members/add'
        data = self.extract()
        if len(self.groups):
            data['group_ids'] = self.groups.keys()
        if signup_form_id:
            data['signup_form_id'] = signup_form_id

        outcome = self.account.adapter.post(path, data)
        self['status'] = member_status.MemberStatus.factory(outcome['status'])
        if outcome['added']:
            self['member_id'] = outcome['member_id']

    def _update(self):
        path = "/members/%s" % self._dict['member_id']
        data = self.extract()
        if self._dict['status'] in (member_status.Active, member_status.Error,
                                    member_status.OptOut):
            data['status_to'] = self._dict['status'].get_code()
        if not self.account.adapter.put(path, data):
            raise MemberUpdateError()

    def save(self, signup_form_id=None):
        """
        Add or update this :class:`Member`

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr['last_name'] = u"New-Name"
            >>> mbr.save()
            None
            >>> mbr = acct.members.factory({'email': u"new@example.com"})
            >>> mbr.save()
            None
        """
        if 'member_id' not in self._dict:
            return self._add(signup_form_id)
        else:
            return self._update()

    def is_deleted(self):
        """
        Whether a member has been deleted

        :rtype: :class:`bool`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.is_deleted()
            False
            >>> mbr.delete()
            >>> mbr.is_deleted()
            True
        """
        return 'deleted_at' in self._dict and self._dict['deleted_at']

    def delete(self):
        """
        Delete this member

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.delete()
            None
        """
        if not 'member_id' in self._dict:
            raise NoMemberIdError()
        if self.is_deleted():
            return None

        path = "/members/%s" % self._dict['member_id']
        if self.account.adapter.delete(path):
            self._dict['deleted_at'] = True

    def add_groups(self, group_ids=None):
        """
        Convenience method for adding groups to a Member

        :param group_ids: Set of Group identifiers to add
        :type group_ids: :class:`list` of :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.add_groups([1024, 1025])
            None
        """
        return self.groups.save(map(
            lambda x: self.groups.factory({'member_group_id': x}),
            group_ids
        ))

    def drop_groups(self, group_ids=None):
        """
        Convenience method for dropping groups from a Member

        :param group_ids: Set of Group identifiers to drop
        :type group_ids: :class:`list` of :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.drop_groups([1024, 1025]) # Drop a specific list of groups
            None
            >>> mbr.drop_groups() # Drop all groups
            None
        """
        return self.groups.delete(group_ids)


class MemberMailingCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Mailing` objects of a
    :class:`Member`

    :param member: The Member which owns this collection
    :type member: :class:`Member`
    """
    def __init__(self, member):
        self.member = member
        super(MemberMailingCollection, self).__init__()

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Mailing` objects

        :rtype: :class:`dict` of :class:`Mailing` objects

        Usage::

            >>> from myemma.model.account import Account
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


class MemberGroupCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Group` objects of a
    :class:`Member`

    :param member: The Member which owns this collection
    :type member: :class:`Member`
    """
    def __init__(self, member):
        self.member = member
        super(MemberGroupCollection, self).__init__()

    def factory(self, raw=None):
        """
        Creates a :class:`Group`

        :rtype: :class:`Group`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.groups.factory()
            <Group{}>
            >>> mbr.groups.factory({'member_group_id':1024})
            <Group{'member_group_id':1024}>
        """
        return Group(self.member.account, raw)

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Group` objects

        :rtype: :class:`dict` of :class:`Group` objects

        Usage::

            >>> from myemma.model.account import Account
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
                lambda x: (x['member_group_id'], Group(self.member.account, x)),
                self.member.account.adapter.get(path)
            ))
        return self._dict

    def save(self, groups=None):
        """
        :param groups: List of :class:`Group` objects to save
        :type groups: :class:`list` of :class:`Group` objects
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grps = acct.members[123].groups
            >>> grps.save([
            ...     grps.factory({'member_group_id': 300}),
            ...     grps.factory({'member_group_id': 301}),
            ...     grps.factory({'member_group_id': 302})
            ... ])
            None
        """
        if 'member_id' not in self.member:
            raise NoMemberIdError()
        if not groups:
            return None

        path = '/members/%s/groups' % self.member['member_id']
        data = {'group_ids': map(lambda x: x['member_group_id'], groups)}
        if self.member.account.adapter.put(path, data):
            self.clear()

    def _delete_by_list(self, group_ids):
        path = '/members/%s/groups/remove' % self.member['member_id']
        data = {'group_ids': group_ids}
        if self.member.account.adapter.put(path, data):
            self._dict = dict(filter(
                lambda x: x[0] not in group_ids,
                self._dict.items()))

    def _delete_all_groups(self):
        path = '/members/%s/groups' % self.member['member_id']
        if self.member.account.adapter.delete(path, {}):
            self._dict = {}

    def delete(self, group_ids=None):
        """
        :param group_ids: List of group identifiers to delete
        :type group_ids: :class:`list` of :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grps = acct.members[123].groups
            >>> grps.delete([300, 301]) # Delete a specific list of groups
            None
            >>> grps.delete() # Delete all groups
            None
        """
        if 'member_id' not in self.member:
            raise NoMemberIdError()

        return (self._delete_by_list(group_ids)
                if group_ids
                else self._delete_all_groups())

