"""Audience import models"""

from myemma import exceptions as ex
from myemma.model import BaseApiModel, str_fields_to_datetime
from myemma.model.member import Member


class MemberImport(BaseApiModel):
    """
    Encapsulates operations for a :class:`MemberImport`

    :param account: The Account which owns this import
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`MemberImport`
    :type raw: :class:`dict`

    Usage::

        >>> from myemma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> mprt = acct.imports[123]
        >>> mprt
        <MemberImport>
    """
    def __init__(self, account, raw=None):
        self.account = account
        super(MemberImport, self).__init__(raw)
        self.members = ImportMemberCollection(self)

    def _parse_raw(self, raw):
        raw.update(
            str_fields_to_datetime(['import_started', 'import_finished'], raw))
        return raw


class ImportMemberCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Member` objects of a
    :class:`MemberImport`

    :param member_import: The Import which owns this collection
    :type member_import: :class:`MemberImport`
    """
    def __init__(self, member_import):
        self.member_import = member_import
        super(ImportMemberCollection, self).__init__()

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Member` objects

        :rtype: :class:`dict` of :class:`Member` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> imprt = acct.imports[1024]
            >>> imprt.members.fetch_all()
            {200: <Member>, 201: <Member>, ...}
        """
        if not 'import_id' in self.member_import:
            raise ex.NoImportIdError()

        path = '/members/imports/%s/members' % self.member_import['import_id']
        if not self._dict:
            self._dict = dict(
                (x['member_id'], Member(self.member_import.account, x))
                    for x in self.member_import.account.adapter.get(path))
        return self._dict
