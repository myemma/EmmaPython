"""Audience group models"""

from datetime import datetime
from myemma import exceptions as ex
from myemma.model import BaseApiModel, str_fields_to_datetime
import myemma.model.member


class Group(BaseApiModel):
    """
    Encapsulates operations for a :class:`Group`

    :param account: The Account which owns this Group
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Group`
    :type raw: :class:`dict`

    Usage::

        >>> from myemma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> grp = acct.groups[123]
        >>> grp
        <Group>
    """
    def __init__(self, account, raw=None):
        self.account = account
        self.members = GroupMemberCollection(self)
        super(Group, self).__init__(raw)

    def _parse_raw(self, raw):
        raw.update(str_fields_to_datetime(['deleted_at'], raw))
        return raw

    def is_deleted(self):
        """
        Whether a group has been deleted

        :rtype: :class:`bool`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[123]
            >>> grp.is_deleted()
            False
            >>> grp.delete()
            >>> grp.is_deleted()
            True
        """
        return 'deleted_at' in self._dict and bool(self._dict['deleted_at'])

    def delete(self):
        """
        Delete this group

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[123]
            >>> grp.delete()
            None
        """
        if not 'member_group_id' in self._dict:
            raise ex.NoGroupIdError()
        if self.is_deleted():
            return None

        path = "/groups/%s" % self._dict['member_group_id']
        if self.account.adapter.delete(path):
            self._dict['deleted_at'] = datetime.now()
        if self._dict['member_group_id'] in self.account.groups:
            del(self.account.groups._dict[self._dict['member_group_id']])

    def extract(self):
        """
        Extracts data from the model in a format suitable for using with the API

        :rtype: :class:`dict`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[123]
            >>> grp.extract()
            {'member_group_id':123, 'group_name':u"My Group", ...}
        """
        if 'group_name' not in self._dict:
            raise ex.NoGroupNameError()

        keys = ['group_name']

        return dict(x for x in self._dict.items() if x[0] in keys)

    def _add(self):
        """Add a single group"""
        self.account.groups.save([self])

    def _update(self):
        """Update a single group"""
        path = "/groups/%s" % self._dict['member_group_id']
        data = self.extract()
        if not self.account.adapter.put(path, data):
            raise ex.GroupUpdateError()

    def save(self):
        """
        Add or update this :class:`Group`

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[123]
            >>> grp['group_name'] = u"Renamed Group"
            >>> grp.save()
            None
            >>> grp = acct.groups.factory({'group_name': u"New Group"})
            >>> grp.save()
            None
        """
        if 'member_group_id' not in self._dict:
            return self._add()
        else:
            return self._update()


class GroupMemberCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Member` objects of a
    :class:`Group`

    :param group: The group which owns this collection
    :type group: :class:`Group`
    """
    def __init__(self, group):
        self.group = group
        super(GroupMemberCollection, self).__init__()

    def __delitem__(self, key):
        self.remove_by_id([key])

    def fetch_all(self, deleted=False):
        """
        Lazy-loads the set of :class:`Member` objects

        :param deleted: Include deleted members
        :type deleted: :class:`bool`
        :rtype: :class:`dict` of :class:`Member` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[1024]
            >>> grp.members.fetch_all()
            {200: <Member>, 201: <Member>, ...}
        """
        if not 'member_group_id' in self.group:
            raise ex.NoGroupIdError()

        member = myemma.model.member
        path = '/groups/%s/members' % self.group['member_group_id']
        params = {'deleted':True} if deleted else {}
        if not self._dict:
            self._dict = dict(
                (x['member_id'], member.Member(self.group.account, x))
                    for x in self.group.account.adapter.get(path, params))
        return self._dict

    def add_by_id(self, member_ids=None):
        """
        Makes given members part of this group

        :param member_ids: Set of identifiers to add
        :type member_ids: :class:`list` of :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[1024]
            >>> grp.members.add_by_id([200, 201])
            None
        """
        if 'member_group_id' not in self.group:
            raise ex.NoGroupIdError()
        if not member_ids:
            return None

        path = '/groups/%s/members' % self.group['member_group_id']
        data = {'member_ids': member_ids}
        self.group.account.adapter.put(path, data)

    def add_by_status(self, statuses=None):
        """
        Makes all members of a particular status part of this group

        :param statuses: Set of statuses to add
        :type statuses: :class:`list` of :class:`str`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> from myemma.enumerations import MemberStatus
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[1024]
            >>> grp.members.add_by_status([MemberStatus.Active])
            None
        """
        if 'member_group_id' not in self.group:
            raise ex.NoGroupIdError()
        if not statuses:
            return None

        path = '/members/%s/copy' % self.group['member_group_id']
        data = {'member_status_id': statuses}
        if not self.group.account.adapter.put(path, data):
            raise ex.MemberCopyToGroupError()

    def add_by_group(self, group, statuses):
        """
        Makes all members of a particular group part of this group

        :param group: The group to copy members from
        :type group: :class:`Group`
        :param statuses: Set of statuses to add
        :type statuses: :class:`list` of :class:`str`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[1024]
            >>> grp.members.add_by_group(acct.groups[199])
            None
            >>> from myemma.enumerations import MemberStatus
            >>> grp.members.add_by_group(acct.groups[200], [MemberStatus.Active])
            None
        """
        if 'member_group_id' not in self.group:
            raise ex.NoGroupIdError()
        if 'member_group_id' not in group:
            raise ex.NoGroupIdError()

        path = '/groups/%s/%s/members/copy' % (
            group['member_group_id'],
            self.group['member_group_id'])
        data = {'member_status_id': statuses} if statuses else {}
        if not self.group.account.adapter.put(path, data):
            raise ex.MemberCopyToGroupError()

    def remove_by_id(self, member_ids=None):
        """
        Remove given members from this group

        :param member_ids: Set of identifiers to remove
        :type member_ids: :class:`list` of :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[1024]
            >>> grp.members.remove_by_id([200, 201])
            None
        """
        if 'member_group_id' not in self.group:
            raise ex.NoGroupIdError()
        if not member_ids:
            return None

        path = '/groups/%s/members/remove' % self.group['member_group_id']
        data = {'member_ids': member_ids}
        removed = self.group.account.adapter.put(path, data)
        self._dict = dict(x for x in self._dict.items() if x[0] not in removed)

    def remove_all(self, status=None):
        """
        Remove all members from this group

        :param status: A status to remove
        :type status: :class:`str`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> from myemma.enumerations import MemberStatus
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[1024]
            >>> grp.members.remove_all(MemberStatus.Active)
            None
            >>> grp.members.remove_all()
            None
        """
        if 'member_group_id' not in self.group:
            raise ex.NoGroupIdError()

        path = '/groups/%s/members' % self.group['member_group_id']
        params = {'member_status_id': status} if status else {}
        if self.group.account.adapter.delete(path, params):
            self._dict = {}
