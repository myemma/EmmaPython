from myemma.adapter import V1Adapter
from collection import Collection
from emma_import import EmmaImport
from member import Member
from field import Field

class Account(object):
    default_adapter = V1Adapter

    def __init__(self, account_id, public_key, private_key):
        self.adapter = self.__class__.default_adapter({
            "account_id": account_id,
            "public_key": public_key,
            "private_key": private_key
        })
        self.fields = FieldCollection(self.adapter)
        self.members = MemberCollection(self.adapter)
        self.imports = ImportCollection(self.adapter)

class FieldCollection(Collection):
    """
    Encapsulates operations for the set of fields of an account
    """
    def fetch_all(self):
        """
        Lazy-loads the collection
        """
        path = '/fields'
        if len(self) == 0:
            self._dict = dict(map(
                lambda x: (x[u"field_id"], Field(self.adapter, x)),
                self.adapter.get(path, {})
            ))
        return self._dict

class MemberCollection(Collection):
    """
    Encapsulates operations for the set of members of an account
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
        Lazy-loads the collection
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
        Refreshes the collection with the current dictionary of all members of a
        given import, then returns that dictionary
        """
        path = '/members/imports/%s/members' % import_id
        members = dict(map(
            lambda x: (x[u"member_id"], Member(self.adapter, x)),
            self.adapter.get(path, {})
        ))
        self.replace_all(members)
        return members

    def find_one_by_member_id(self, member_id, deleted = False):
        """
        Lazy-loads a single Member that matches the member_id or None
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
        Lazy-loads a single Member that matches the email or None
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
    Encapsulates operations for the set of imports for an account
    """
    def __getitem__(self, key):
        """
        Overriding again to provide lazy-loading of an import by ID
        """
        return self.find_one_by_import_id(key)

    def fetch_all(self):
        """
        Lazy-loads the collection
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
        Lazy-loads a single Import that matches the import_id or None
        """
        path = '/members/imports/%s' % import_id
        if not self._dict.has_key(import_id):
            emma_import = self.adapter.get(path, {})
            if emma_import is not None:
                self._dict[emma_import[u"import_id"]] =\
                    EmmaImport(self.adapter, emma_import)
                return self._dict[emma_import[u"import_id"]]
        else:
            return self._dict[import_id]

__all__ = ['Account']