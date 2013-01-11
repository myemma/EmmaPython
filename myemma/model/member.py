from base import BaseApiModel
from collection import Collection
from group import Group
from mailing import Mailing

class NoMemberEmailError(Exception): pass
class NoMemberIdError(Exception): pass
class NoMemberStatusError(Exception): pass

class Member(BaseApiModel):

    def __init__(self, adapter, raw = None):
        self.adapter = adapter
        self.groups = MemberGroupCollection(self.adapter, self)
        self.mailings = MemberMailingCollection(self.adapter, self)
        self._dict = raw if raw is not None else {}

    def opt_out(self):
        if not self._dict.has_key(u"email"):
            raise NoMemberEmailError()
        path = '/members/email/optout/%s' % self._dict[u"email"]
        if self.adapter.put(path, {}):
            self._dict[u"status"] = u"opt-out"

    def get_opt_out_detail(self):
        if not self._dict.has_key(u"member_id"):
            raise NoMemberIdError()
        path = '/members/%s/optout' % self._dict[u"member_id"]
        return self.adapter.get(path, {})

    def has_opted_out(self):
        if not self._dict.has_key(u"status"):
            raise NoMemberStatusError()
        return self._dict[u"status"] == u"opt-out"


class MemberMailingCollection(Collection):
    """
    Encapsulates operations for the set of mailings for a member
    """
    def __init__(self, adapter, member):
        self.member = member
        super(MemberMailingCollection, self).__init__(adapter)

    def fetch_all(self):
        """
        Lazy-loads the collection
        """
        if u"member_id" not in self.member:
            raise NoMemberIdError()
        path = '/members/%s/mailings' % self.member[u"member_id"]
        if len(self) == 0:
            self._dict = dict(map(
                lambda x: (x[u"mailing_id"], Mailing(self.adapter, x)),
                self.adapter.get(path, {})
            ))
        return self._dict

class MemberGroupCollection(Collection):
    """
    Encapsulates operations for the set of groups for a member
    """
    def __init__(self, adapter, member):
        self.member = member
        super(MemberGroupCollection, self).__init__(adapter)

    def fetch_all(self):
        """
        Lazy-loads the collection
        """
        if u"member_id" not in self.member:
            raise NoMemberIdError()
        path = '/members/%s/groups' % self.member[u"member_id"]
        if len(self) == 0:
            self._dict = dict(map(
                lambda x: (x[u"group_name"], Group(self.adapter, x)),
                self.adapter.get(path, {})
            ))
        return self._dict

__all__ = ['Member']