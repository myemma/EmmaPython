from collection import Collection
from emma_import import EmmaImport
from member import Member
from field import Field
from myemma.adapter.requests_adapter import RequestsAdapter

class Account(object):
    """
    Aggregate root for the API context

    You will use this object to get all other information from the API::

        acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        acct.members.fetch_all() # get all members for this account

    :param account_id: Your account identifier
    :type account_id: :class:`int` or :class:`str`
    :param public_key: Your public key
    :type public_key: :class:`str`
    :param private_key: Your private key
    :type private_key: :class:`str`
    """
    default_adapter = RequestsAdapter

    def __init__(self, account_id, public_key, private_key):
        self.adapter = self.__class__.default_adapter({
            "account_id": "%s" % account_id,
            "public_key": public_key,
            "private_key": private_key
        })
        self.fields = FieldCollection(self.adapter)
        self.members = MemberCollection(self.adapter)
        self.imports = ImportCollection(self.adapter)

class FieldCollection(Collection):
    """
    Encapsulates operations for the set of :class:`Field` objects of an :class:`account`
    """
    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Field` objects

        :rtype: :class:`list` of :class:`Field` objects

        Usage::

            acct.fields.fetch_all() # [Field, Field, ...]

        """
        path = '/fields'
        if len(self) == 0:
            self._dict = dict(map(
                lambda x: (x[u"field_id"], Field(self.adapter, x)),
                self.adapter.get(path)
            ))
        return self._dict

class MemberCollection(Collection):
    """
    Encapsulates operations for the set of :class:`Member` objects of an :class:`account`
    """
    def __getitem__(self, key):
        """
        Overriding again to provide lazy-loading of a member by ID or email
        """
        if isinstance(key, int):
            return self.find_one_by_member_id(key)
        if isinstance(key, str):
            return self.find_one_by_email(key)
        if isinstance(key, unicode):
            return self.find_one_by_email(key)

    def fetch_all(self, deleted = False):
        """
        Lazy-loads the full set of :class:`Member` objects

        :param deleted: Whether to include deleted members
        :type deleted: :class:`bool`
        :rtype: :class:`list` of :class:`Member` objects

        Usage::

            acct.members.fetch_all() # [Member, Member, ...]

        """
        path = '/members'
        params = {"deleted":True} if deleted else {}
        if len(self) == 0:
            self._dict = dict(map(
                lambda x: (x[u"member_id"], Member(self.adapter, x)),
                self.adapter.get(path, params)
            ))
        return self._dict

    def fetch_all_by_import_id(self, import_id):
        """
        Updates the collection with a dictionary of all members from a given
        import. *Does not lazy-load*

        :param import_id: The import identifier
        :type import_id: :class:`int` or :class:`str`
        :rtype: :class:`list` of :class:`Member` objects

        Usage::

            acct.members.fetch_all_by_import_id(123) # [Member, Member, ...]

        """
        path = '/members/imports/%s/members' % import_id
        members = dict(map(
            lambda x: (x[u"member_id"], Member(self.adapter, x)),
            self.adapter.get(path)
        ))
        self.replace_all(members)
        return members

    def find_one_by_member_id(self, member_id, deleted = False):
        """
        Lazy-loads a single :class:`Member` by ID

        :param member_id: The member identifier
        :type member_id: :class:`int`
        :param deleted: Whether to include deleted members
        :type deleted: :class:`bool`
        :rtype: :class:`Member` or :class:`None`

        Usage::

            acct.members.find_one_by_member_id(123) # Member or None
            # -- or --
            acct.members[123] # Member or None

        """
        path = '/members/%s' % member_id
        params = {"deleted":True} if deleted else {}
        if member_id not in self._dict.keys():
            member = self.adapter.get(path, params)
            if member is not None:
                self._dict[member[u"member_id"]] = Member(self.adapter, member)
                return self._dict[member[u"member_id"]]
        else:
            return self._dict[member_id]

    def find_one_by_email(self, email, deleted = False):
        """
        Lazy-loads a single :class:`Member` by email address

        :param email: The email address
        :type email: :class:`str`
        :param deleted: Whether to include deleted members
        :type deleted: :class:`bool`
        :rtype: :class:`Member` or :class:`None`

        Usage::

            acct.members.find_one_by_email("test@example.com") # Member or None
            # -- or --
            acct.members["test@example.com"] # Member or None

        """
        path = '/members/email/%s' % email
        params = {"deleted":True} if deleted else {}
        members = filter(
            lambda x: x[u"email"] == email,
            self._dict.values())
        if not members:
            member = self.adapter.get(path, params)
            if member is not None:
                self._dict[member[u"member_id"]] = Member(self.adapter, member)
                return self._dict[member[u"member_id"]]
        else:
            member = members[0]
        return member

class ImportCollection(Collection):
    """
    Encapsulates operations for the set of :class:`Import` objects of an :class:`account`
    """
    def __getitem__(self, key):
        """
        Overriding again to provide lazy-loading of an import by ID
        """
        return self.find_one_by_import_id(key)

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Import` objects

        :rtype: :class:`list` of :class:`Import` objects

        Usage::

            acct.imports.fetch_all() # [Import, Import, ...]

        """
        path = '/members/imports'
        if len(self) == 0:
            self._dict = dict(map(
                lambda x: (x[u"import_id"], EmmaImport(self.adapter, x)),
                self.adapter.get(path, {})
            ))
        return self._dict

    def find_one_by_import_id(self, import_id):
        """
        Lazy-loads a single :class:`Import` by ID

        :param import_id: The import identifier
        :type import_id: :class:`int` or :class:`str`
        :rtype: :class:`Import` or :class:`None`

        Usage::

            acct.imports.find_one_by_import_id(123) # Import or None
            # -- or --
            acct.imports[123] # Import or None

        """
        import_id = int(import_id)
        path = '/members/imports/%s' % import_id
        if not self._dict.has_key(import_id):
            emma_import = self.adapter.get(path)
            if emma_import is not None:
                self._dict[emma_import[u"import_id"]] =\
                    EmmaImport(self.adapter, emma_import)
                return self._dict[emma_import[u"import_id"]]
        else:
            return self._dict[import_id]

__all__ = ['Account', 'FieldCollection', 'MemberCollection', 'ImportCollection']