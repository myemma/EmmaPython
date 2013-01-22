"""Audience member models"""

from datetime import datetime
from myemma import exceptions as ex
from myemma.enumerations import MemberStatus
from myemma.model import BaseApiModel, str_fields_to_datetime
import myemma.model.group
import myemma.model.mailing


class Member(BaseApiModel):
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
        if 'fields' in raw:
            raw.update(raw['fields'])
            del(raw['fields'])
        raw.update(str_fields_to_datetime(
            ['last_modified_at', 'member_since', 'deleted_at'],
            raw))
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
            raise ex.NoMemberEmailError()
        path = '/members/email/optout/%s' % self._dict['email']
        if self.account.adapter.put(path):
            self._dict['member_status_id'] = MemberStatus.OptOut

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
            raise ex.NoMemberIdError()
        if self._dict['member_status_id'] != MemberStatus.OptOut:
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
        if 'member_status_id' not in self._dict:
            raise ex.NoMemberStatusError()
        return self._dict['member_status_id'] == MemberStatus.OptOut

    def extract(self):
        """
        Extracts data from the model in a format suitable for using with the API

        :rtype: :class:`dict`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mbr = acct.members[123]
            >>> mbr.extract()
            {'member_id':123, 'email':u"test@example.org", 'fields':{...}}
        """
        if 'email' not in self._dict:
            raise ex.NoMemberEmailError

        extracted = dict(x for x in self._dict.items()
            if x[0] in ['member_id', 'email'])
        fields = dict(x for x in self._dict.items()
            if x[0] in self.account.fields.export_shortcuts())
        if fields:
            extracted['fields'] = fields

        return extracted

    def _add(self, signup_form_id):
        """Add a single member"""
        path = '/members/add'
        data = self.extract()
        if len(self.groups):
            data['group_ids'] = self.groups.keys()
        if signup_form_id:
            data['signup_form_id'] = signup_form_id

        outcome = self.account.adapter.post(path, data)
        self['member_status_id'] = outcome['status']
        if outcome['added']:
            self['member_id'] = outcome['member_id']

    def _update(self):
        """Update a single member"""
        s = MemberStatus
        path = "/members/%s" % self._dict['member_id']
        data = self.extract()
        if self._dict['member_status_id'] in (s.Active, s.Error, s.OptOut):
            data['status_to'] = self._dict['member_status_id']
        if not self.account.adapter.put(path, data):
            raise ex.MemberUpdateError()

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
        return 'deleted_at' in self._dict and bool(self._dict['deleted_at'])

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
            raise ex.NoMemberIdError()
        if self.is_deleted():
            return None

        path = "/members/%s" % self._dict['member_id']
        if self.account.adapter.delete(path):
            self._dict['deleted_at'] = datetime.now()

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
        return self.groups.save(
            [self.groups.factory({'member_group_id': x}) for x in group_ids])

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

    def __delitem__(self, key):
        pass

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
            raise ex.NoMemberIdError()
        mailing = myemma.model.mailing
        path = '/members/%s/mailings' % self.member['member_id']
        if not self._dict:
            self._dict = dict(
                (x['mailing_id'], mailing.Mailing(self.member.account, x))
                    for x in self.member.account.adapter.get(path))
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

    def __delitem__(self, key):
        self._delete_by_list([key])

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
        return myemma.model.group.Group(self.member.account, raw)

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
            raise ex.NoMemberIdError()
        group = myemma.model.group
        path = '/members/%s/groups' % self.member['member_id']
        if not self._dict:
            self._dict = dict(
                (x['member_group_id'], group.Group(self.member.account, x))
                    for x in self.member.account.adapter.get(path))
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
            raise ex.NoMemberIdError()
        if not groups:
            return None

        path = '/members/%s/groups' % self.member['member_id']
        data = {'group_ids': [x['member_group_id'] for x in groups]}
        if self.member.account.adapter.put(path, data):
            self.clear()

    def _delete_by_list(self, group_ids):
        """Drop groups by list of identifiers"""
        path = '/members/%s/groups/remove' % self.member['member_id']
        data = {'group_ids': group_ids}
        if self.member.account.adapter.put(path, data):
            self._dict = dict(x for x in self._dict.items()
                if x[0] not in group_ids)

    def _delete_all_groups(self):
        """Drop all groups"""
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
            raise ex.NoMemberIdError()

        return (self._delete_by_list(group_ids)
                if group_ids
                else self._delete_all_groups())

