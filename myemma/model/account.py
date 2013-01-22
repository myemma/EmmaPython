"""The aggregate root (Account) and collections owned by the root"""

from myemma import exceptions as ex
from myemma.adapter.requests_adapter import RequestsAdapter
from myemma.model import BaseApiModel
from myemma.enumerations import MemberStatus
from myemma.model.mailing import Mailing
from myemma.model.member import Member
from myemma.model.member_import import MemberImport
import myemma.model.field
import myemma.model.group
import myemma.model.search


class Account(object):
    """
    Aggregate root for the API context

    :param account_id: Your account identifier
    :type account_id: :class:`int` or :class:`str`
    :param public_key: Your public key
    :type public_key: :class:`str`
    :param private_key: Your private key
    :type private_key: :class:`str`

    Usage::

        >>> from myemma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> acct.fields
        <AccountFieldCollection>
        >>> acct.imports
        <AccountImportCollection>
        >>> acct.mailings
        <AccountMailingCollection>
        >>> acct.members
        <AccountMemberCollection>
    """
    default_adapter = RequestsAdapter

    def __init__(self, account_id, public_key, private_key):
        self.adapter = self.__class__.default_adapter({
            "account_id": "%s" % account_id,
            "public_key": public_key,
            "private_key": private_key
        })
        self.fields = AccountFieldCollection(self)
        self.groups = AccountGroupCollection(self)
        self.imports = AccountImportCollection(self)
        self.mailings = AccountMailingCollection(self)
        self.members = AccountMemberCollection(self)
        self.searches = AccountSearchCollection(self)


class AccountFieldCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Field` objects of an
    :class:`account`

    :param account: The Account which owns this collection
    :type account: :class:`Account`
    """
    def __init__(self, account):
        self.account = account
        super(AccountFieldCollection, self).__init__()

    def __getitem__(self, key):
        return self.find_one_by_field_id(key, True)

    def __delitem__(self, key):
        self._dict[key].delete()

    def factory(self, raw=None):
        """
        New :class:`Field` factory

        :param raw: Raw data with which to populate class
        :type raw: :class:`dict`
        :rtype: :class:`Field`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.fields.factory()
            <Field{}>
            >>> acct.fields.factory({'shortcut_name': u"test_field"})
            <Field{'shortcut_name': u"test_field"}>
        """
        return myemma.model.field.Field(self.account, raw)

    def fetch_all(self, deleted=False):
        """
        Lazy-loads the full set of :class:`Field` objects

        :param deleted: Whether to include deleted fields
        :type deleted: :class:`bool`
        :rtype: :class:`dict` of :class:`Field` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.fields.fetch_all()
            {123: <Field>, 321: <Field>, ...}
        """
        field = myemma.model.field
        path = '/fields'
        params = {"deleted":True} if deleted else {}
        if not self._dict:
            self._dict = dict(
                (x['field_id'], field.Field(self.account, x))
                    for x in self.account.adapter.get(path, params))
        return self._dict

    def find_one_by_field_id(self, field_id, deleted=False):
        """
        Lazy-loads a single :class:`Field` by ID

        :param field_id: The field identifier
        :type field_id: :class:`int`
        :param deleted: Whether to find a deleted field
        :type deleted: :class:`bool`
        :rtype: :class:`Field` or :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.fields.find_one_by_field_id(0) # does not exist
            None
            >>> acct.fields.find_one_by_field_id(123)
            <Field>
            >>> acct.fields[123]
            <Field>
        """
        field = myemma.model.field
        field_id = int(field_id)
        path = '/fields/%s' % field_id
        params = {"deleted":True} if deleted else {}
        if field_id not in self._dict:
            f = self.account.adapter.get(path, params)
            if f:
                self._dict[field_id] = field.Field(self.account, f)
                return self._dict[field_id]
        else:
            return self._dict[field_id]

    def export_shortcuts(self):
        """
        Get a :class:`list` of shortcut names for this account

        :rtype: :class:`list` of :class:`str`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.fields.export_shortcuts()
            ["first_name", "last_name", ...]
        """
        return [x['shortcut_name'] for x in self.fetch_all().values()]


class AccountGroupCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Group` objects of an
    :class:`account`

    :param account: The Account which owns this collection
    :type account: :class:`Account`
    """
    def __init__(self, account):
        self.account = account
        super(AccountGroupCollection, self).__init__()

    def __getitem__(self, key):
        return self.find_one_by_group_id(key)

    def __delitem__(self, key):
        self[key].delete()

    def factory(self, raw=None):
        """
        New :class:`Group` factory

        :param raw: Raw data with which to populate class
        :type raw: :class:`dict`
        :rtype: :class:`Group`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.groups.factory()
            <Group{}>
            >>> acct.groups.factory({'group_name': u"Test Group"})
            <Group{'group_name': u"Test Group"}>
        """
        return myemma.model.group.Group(self.account, raw)

    def fetch_all(self, group_types=None):
        """
        Lazy-loads the full set of :class:`Group` objects

        :rtype: :class:`dict` of :class:`Group` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.groups.fetch_all()
            {123: <Group>, 321: <Group>, ...}
            >>> from myemma.enumerations import GroupType
            >>> acct.groups.fetch_all([GroupType.TestGroup])
            {007: <Group>}
        """
        group = myemma.model.group
        path = '/groups'
        params = {'group_types': group_types} if group_types else {}
        if not self._dict:
            self._dict = dict(
                (x['member_group_id'], group.Group(self.account, x))
                    for x in self.account.adapter.get(path, params))
        return self._dict

    def find_one_by_group_id(self, group_id):
        """
        Lazy-loads a single :class:`Group` by ID

        :param group_id: The group identifier
        :type group_id: :class:`int` or :class:`str`
        :rtype: :class:`Group` or :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.groups.find_one_by_group_id(0) # does not exist
            None
            >>> acct.groups.find_one_by_group_id(123)
            <Group>
            >>> acct.groups[123]
            <Group>
        """
        group = myemma.model.group
        group_id = int(group_id)
        path = '/groups/%s' % group_id
        if group_id not in self._dict:
            g = self.account.adapter.get(path)
            if g:
                self._dict[group_id] = group.Group(self.account, g)
                return self._dict[group_id]
        else:
            return self._dict[group_id]

    def save(self, groups=None):
        """
        :param groups: List of :class:`Group` objects to save
        :type groups: :class:`list` of :class:`Group` objects
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.groups.save() # no changes
            None
            >>> acct.groups.save([
            ...     acct.groups.factory({'group_name': u"New Group 1"}),
            ...     acct.groups.factory({'group_name': u"New Group 2"}),
            ...     acct.groups.factory({'group_name': u"New Group 3"})
            ... ])
            None
        """
        if not groups:
            return None

        group = myemma.model.group
        path = '/groups'
        data = {'groups': [x.extract() for x in groups]}
        added = self.account.adapter.post(path, data)
        self._dict.update(dict(
            (x['member_group_id'], group.Group(self.account, x))
                for x in added))


class AccountImportCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Import` objects of an
    :class:`account`

    :param account: The Account which owns this collection
    :type account: :class:`Account`
    """
    def __init__(self, account):
        self.account = account
        super(AccountImportCollection, self).__init__()

    def __getitem__(self, key):
        return self.find_one_by_import_id(key)

    def __delitem__(self, key):
        self.delete([key])

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Import` objects

        :rtype: :class:`dict` of :class:`Import` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.imports.fetch_all()
            {123: <Import>, 321: <Import>, ...}

        """
        path = '/members/imports'
        if not self._dict:
            self._dict = dict(
                (x['import_id'], MemberImport(self.account, x))
                    for x in self.account.adapter.get(path, {}))
        return self._dict

    def find_one_by_import_id(self, import_id):
        """
        Lazy-loads a single :class:`Import` by ID

        :param import_id: The import identifier
        :type import_id: :class:`int` or :class:`str`
        :rtype: :class:`Import` or :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.imports.find_one_by_import_id(0) # does not exist
            None
            >>> acct.imports.find_one_by_import_id(123)
            <Import>
            >>> acct.imports[123]
            <Import>
        """
        import_id = int(import_id)
        path = '/members/imports/%s' % import_id
        if import_id not in self._dict:
            emma_import = self.account.adapter.get(path)
            if emma_import is not None:
                self._dict[import_id] = MemberImport(self.account, emma_import)
                return self._dict[import_id]
        else:
            return self._dict[import_id]

    def delete(self, import_ids=None):
        """
        :param import_ids: Set of import identifiers to delete
        :type import_ids: :class:`list` of :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.imports.delete([123, 321]) # Deletes imports 123, and 321
            None
        """
        if not import_ids:
            return None

        path = '/members/imports/delete'
        params = {'import_ids': import_ids}
        if not self.account.adapter.delete(path, params):
            raise ex.ImportDeleteError()

        # Update internal dictionary
        self._dict = dict(
            x for x in self._dict.items() if x[0] not in import_ids)


class AccountMemberCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Member` objects of an
    :class:`account`

    :param account: The Account which owns this collection
    :type account: :class:`Account`
    """
    def __init__(self, account):
        self.account = account
        super(AccountMemberCollection, self).__init__()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.find_one_by_member_id(key)
        if isinstance(key, str) or isinstance(key, unicode):
            return self.find_one_by_email(str(key))

    def __delitem__(self, key):
        self._dict[key].delete()
        super(AccountMemberCollection, self).__delitem__(key)

    def factory(self, raw=None):
        """
        New :class:`Member` factory

        :param raw: Raw data with which to populate class
        :type raw: :class:`dict`
        :rtype: :class:`Member`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.factory()
            <Member{}>
            >>> acct.members.factory({'email': u"test@example.com"})
            <Member{'email': u"test@example.com"}>
        """
        return Member(self.account, raw)

    def fetch_all(self, deleted=False):
        """
        Lazy-loads the full set of :class:`Member` objects

        :param deleted: Whether to include deleted members
        :type deleted: :class:`bool`
        :rtype: :class:`dict` of :class:`Member` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.fetch_all()
            {123: <Member>, 321: <Member>, ...}
        """
        path = '/members'
        params = {"deleted":True} if deleted else {}
        if not self._dict:
            self._dict = dict(
                (x['member_id'], Member(self.account, x)) for x in
                    self.account.adapter.get(path, params))
        return self._dict

    def fetch_all_by_import_id(self, import_id):
        """
        Updates the collection with a dictionary of all members from a given
        import. *Does not lazy-load*

        :param import_id: The import identifier
        :type import_id: :class:`int` or :class:`str`
        :rtype: :class:`dict` of :class:`Member` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.fetch_all_by_import_id(123)
            {123: <Member>, 321: <Member>, ...}
        """
        path = '/members/imports/%s/members' % import_id
        members = dict(
            (x['member_id'], Member(self.account, x))
                for x in self.account.adapter.get(path))
        self._replace_all(members)
        return members

    def find_one_by_member_id(self, member_id, deleted=False):
        """
        Lazy-loads a single :class:`Member` by ID

        :param member_id: The member identifier
        :type member_id: :class:`int`
        :param deleted: Whether to include deleted members
        :type deleted: :class:`bool`
        :rtype: :class:`Member` or :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.find_one_by_member_id(0) # does not exist
            None
            >>> acct.members.find_one_by_member_id(123)
            <Member{'member_id': 123, 'email': u"test@example.com", ...}>
            >>> acct.members[123]
            <Member{'member_id': 123, 'email': u"test@example.com", ...}>
        """
        path = '/members/%s' % member_id
        params = {"deleted":True} if deleted else {}
        if member_id not in self._dict:
            member = self.account.adapter.get(path, params)
            if member is not None:
                self._dict[member['member_id']] = Member(self.account, member)
                return self._dict[member['member_id']]
        else:
            return self._dict[member_id]

    def find_one_by_email(self, email, deleted=False):
        """
        Lazy-loads a single :class:`Member` by email address

        :param email: The email address
        :type email: :class:`str`
        :param deleted: Whether to include deleted members
        :type deleted: :class:`bool`
        :rtype: :class:`Member` or :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.find_one_by_email("null@example.com") # does not exist
            None
            >>> acct.members.find_one_by_email("test@example.com")
            <Member{'member_id': 123, 'email': u"test@example.com", ...}>
            >>> acct.members["test@example.com"]
            <Member{'member_id': 123, 'email': u"test@example.com", ...}>
        """
        path = '/members/email/%s' % email
        params = {"deleted":True} if deleted else {}
        members = [x for x in self._dict.values() if x['email'] == email]
        if not members:
            member = self.account.adapter.get(path, params)
            if member is not None:
                self._dict[member['member_id']] = \
                    Member(self.account, member)
                return self._dict[member['member_id']]
        else:
            member = members[0]
        return member

    def save(self, members=None, filename=None, add_only=False,
             group_ids=None):
        """
        :param members: List of :class:`Member` objects to save
        :type members: :class:`list` of :class:`Member` objects
        :param filename: An arbitrary string to associate with this import
        :type filename: :class:`str`
        :param add_only: Only add new members, ignore existing members
        :type add_only: :class:`bool`
        :param group_ids: Add imported members to this list of groups
        :type group_ids: :class:`list`
        :rtype: :class:`int` representing an import identifier or :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.save() # no changes
            None
            >>> acct.members[123]['first_name'] = u"Emma"
            >>> acct.members.save()
            2001
            >>> acct.members.save([
            ...     acct.members.factory({'email': u"new1@example.com"}),
            ...     acct.members.factory({'email': u"new2@example.com"}),
            ...     acct.members.factory({'email': u"new3@example.com"})
            ... ])
            2002
        """
        if not members and (not self._dict or add_only) :
            return None

        path = '/members'
        data = {
            'members': (
                ([] if not members else [x.extract() for x in members])
                + ([] if add_only
                   else [x.extract() for x in self._dict.values()]))
        }
        if add_only:
            data['add_only'] = add_only
        if filename:
            data['filename'] = filename
        if group_ids:
            data['group_ids'] = group_ids
        return self.account.adapter.post(path, data)

    def delete_by_status(self, status):
        """
        :param status: Members with this status will be deleted
        :type status: :class:`str`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> from myemma.enumerations import MemberStatus
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.delete_by_status(MemberStatus.OptOut)
            None
        """
        path = '/members'
        params = {'member_status_id': status}
        if not self.account.adapter.delete(path, params):
            raise ex.MemberDeleteError()

        # Update internal dictionary
        self._dict = dict(
            x for x in self._dict.items() if x[1]['member_status_id'] != status)

    def delete(self, member_ids=None):
        """
        :param member_ids: Set of member identifiers to delete
        :type member_ids: :class:`list` of :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.delete([123, 321]) # Deletes members 123, and 321
            None
        """
        if not member_ids:
            return None

        path = '/members/delete'
        data = {'member_ids': member_ids}
        if not self.account.adapter.put(path, data):
            raise ex.MemberDeleteError()

        # Update internal dictionary
        self._dict = dict(
            x for x in self._dict.items() if x[0] not in member_ids)

    def change_status_by_member_id(self, member_ids=None, status_to=None):
        """
        :param member_ids: Set of member identifiers to change
        :type member_ids: :class:`list` of :class:`int`
        :param status_to: The new status
        :type status_to: :class:`str`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> from myemma.enumerations import MemberStatus
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.change_status_by_member_id(
            ...     [123, 321],
            ...     MemberStatus.Active)
            None
        """
        if not member_ids:
            return None
        if not status_to:
            status_to = MemberStatus.Active

        path = '/members/status'
        data = {'member_ids': member_ids, 'status_to': status_to}
        if not self.account.adapter.put(path, data):
            raise ex.MemberChangeStatusError()

        # Update internal dictionary
        for member_id in self._dict:
            if member_id in member_ids:
                self._dict[member_id]['status'] = status_to

    def change_status_by_status(self, old, new, group_id=None):
        """
        :param old: The old status
        :type old: :class:`str`
        :param new: The new status
        :type new: :class:`str`
        :param group_id: An optional group identifier to limit by
        :type group_id: :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> from myemma.enumerations import MemberStatus
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.change_status_by_status(
            ...     MemberStatus.Error,
            ...     MemberStatus.Active)
            None
        """
        path = '/members/status/%s/to/%s' % (old, new)
        data = {'group_id': group_id} if group_id else {}
        if not self.account.adapter.put(path, data):
            raise ex.MemberChangeStatusError()

    def drop_groups(self, member_ids=None, group_ids=None):
        """
        Drop specified groups for specified members

        :param member_ids: Set of Member identifiers to affect
        :type member_ids: :class:`list` of :class:`int`
        :param group_ids: Set of Group identifiers to drop
        :type group_ids: :class:`list` of :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.members.drop_groups([200, 201], [1024, 1025])
            None
        """
        if not member_ids or not group_ids:
            return None

        path = '/members/groups/remove'
        data = {'member_ids': member_ids, 'group_ids': group_ids}
        if not self.account.adapter.put(path, data):
            raise ex.MemberDropGroupError()


class AccountMailingCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Mailing` objects of an
    :class:`account`

    :param account: The Account which owns this collection
    :type account: :class:`Account`
    """
    def __init__(self, account):
        self.account = account
        super(AccountMailingCollection, self).__init__()

    def __getitem__(self, key):
        return self.find_one_by_mailing_id(key)

    def __delitem__(self, key):
        pass

    def fetch_all(self, include_archived=False, mailing_types=None, mailing_statuses=None, is_scheduled=False, with_html_body=False, with_plaintext=False):
        """
        Lazy-loads the full set of :class:`Mailing` objects

        :rtype: :class:`dict` of :class:`Mailing` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.mailings.fetch_all()
            {123: <Mailing>, 321: <Mailing>, ...}

        """
        path = '/mailings'
        params = {}
        if include_archived:
            params['include_archived'] = True
        if mailing_types:
            params['mailing_types'] = mailing_types
        if mailing_statuses:
            params['mailing_statuses'] = mailing_statuses
        if is_scheduled:
            params['is_scheduled'] = True
        if with_html_body:
            params['with_html_body'] = True
        if with_plaintext:
            params['with_plaintext'] = True
        if not self._dict:
            self._dict = dict(
                (x['mailing_id'], Mailing(self.account, x))
                    for x in self.account.adapter.get(path, params))
        return self._dict

    def find_one_by_mailing_id(self, mailing_id):
        """
        Lazy-loads a single :class:`Mailing` by ID

        :param mailing_id: The mailing identifier
        :type mailing_id: :class:`int` or :class:`str`
        :rtype: :class:`Mailing` or :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.mailings.find_one_by_mailing_id(0) # does not exist
            None
            >>> acct.mailings.find_one_by_mailing_id(123)
            <Import>
            >>> acct.mailings[123]
            <Import>
        """
        mailing_id = int(mailing_id)
        path = '/mailings/%s' % mailing_id
        if mailing_id not in self._dict:
            mailing = self.account.adapter.get(path)
            if mailing is not None:
                self._dict[mailing_id] = Mailing(self.account, mailing)
                return self._dict[mailing_id]
        else:
            return self._dict[mailing_id]


class AccountSearchCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Search` objects of an
    :class:`account`

    :param account: The Account which owns this collection
    :type account: :class:`Account`
    """
    def __init__(self, account):
        self.account = account
        super(AccountSearchCollection, self).__init__()

    def __delitem__(self, key):
        self._dict[key].delete()

    def fetch_all(self, deleted=False):
        """
        Lazy-loads the full set of :class:`Search` objects

        :param deleted: Whether to include deleted fields
        :type deleted: :class:`bool`
        :rtype: :class:`dict` of :class:`Search` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> acct.searches.fetch_all()
            {123: <Search>, 321: <Search>, ...}
        """
        search = myemma.model.search
        path = '/searches'
        params = {"deleted":True} if deleted else {}
        if not self._dict:
            self._dict = dict(
                (x['search_id'], search.Search(self.account, x))
                    for x in self.account.adapter.get(path, params))
        return self._dict
