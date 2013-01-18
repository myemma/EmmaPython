from . import BaseApiModel, ModelWithDateFields
from import_status import ImportStatus
from import_style import ImportStyle
from member import Member
from myemma.adapter import NoImportIdError


class MemberImport(BaseApiModel, ModelWithDateFields):
    def __init__(self, account, raw=None):
        self.account = account
        super(MemberImport, self).__init__(raw)
        self.members = ImportMemberCollection(self)

    def _parse_raw(self, raw):
        if 'status' in raw:
            raw['status'] = ImportStatus.factory(raw['status'])
        if 'style' in raw:
            raw['style'] = ImportStyle.factory(raw['style'])
        self._str_fields_to_datetime(
            ['import_started', 'import_finished'],
            raw)
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
            raise NoImportIdError()

        path = '/members/imports/%s/members' % self.member_import['import_id']
        if not self._dict:
            self._dict = dict(map(
                lambda x: (x['member_id'], Member(self.member_import.account, x)),
                self.member_import.account.adapter.get(path)
            ))
        return self._dict
