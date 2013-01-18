import unittest
from datetime import datetime
from myemma.adapter import AbstractAdapter
from myemma.model.account import Account
from myemma.model.member import Member
from myemma.model.member_import import (MemberImport, ImportMemberCollection,
                                        NoMemberImportIdError)
from myemma.model import import_status, import_style, SERIALIZED_DATETIME_FORMAT


class MockAdapter(AbstractAdapter):
    expected = None

    def __init__(self, *args, **kwargs):
        self.called = 0
        self.call = ()

    def _capture(self, method, path, params):
        self.called += 1
        self.call = (method, path, params)

    def get(self, path, params=None):
        self._capture('GET', path, params if params else {})
        return self.__class__.expected

    def post(self, path, data=None):
        self._capture('POST', path, data if data else {})
        return self.__class__.expected

    def put(self, path, data=None):
        self._capture('PUT', path, data if data else {})
        return self.__class__.expected

    def delete(self, path, params=None):
        self._capture('DELETE', path, params if params else {})
        return self.__class__.expected


class MemberImportTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.emma_import = MemberImport(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'status': import_status.Ok.get_code(),
                'style': import_style.AddAndUpdate.get_code(),
                'import_started': datetime.now().strftime(SERIALIZED_DATETIME_FORMAT),
                'import_finished': datetime.now().strftime(SERIALIZED_DATETIME_FORMAT)
            }
        )

    def test_can_parse_special_fields_correctly(self):
        self.assertEquals(self.emma_import['status'], import_status.Ok)
        self.assertEquals(self.emma_import['style'], import_style.AddAndUpdate)
        self.assertIsInstance(
            self.emma_import['import_started'],
            datetime)
        self.assertIsInstance(
            self.emma_import['import_finished'],
            datetime)

    def test_can_access_member_collection(self):
        self.assertIsInstance(self.emma_import.members, ImportMemberCollection)


class ImportMemberCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.members = MemberImport(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'status': import_status.Ok.get_code(),
                'style': import_style.AddAndUpdate.get_code(),
                'import_started': datetime.now().strftime(SERIALIZED_DATETIME_FORMAT),
                'import_finished': datetime.now().strftime(SERIALIZED_DATETIME_FORMAT)
            }
        ).members

    def test_can_fetch_all_members(self):
        with self.assertRaises(NoMemberImportIdError):
            self.members.fetch_all()
        self.assertEquals(self.members.member_import.account.adapter.called, 0)

    def test_can_fetch_all_members2(self):
        # Setup
        MockAdapter.expected = [
            {'member_id': 200, 'email': u"test01@example.org"},
            {'member_id': 201, 'email': u"test02@example.org"},
            {'member_id': 202, 'email': u"test03@example.org"}
        ]
        self.members.member_import['import_id'] = 1024

        members = self.members.fetch_all()

        self.assertEquals(self.members.member_import.account.adapter.called, 1)
        self.assertEquals(
            self.members.member_import.account.adapter.call,
            ('GET', '/members/imports/1024/members', {}))
        self.assertIsInstance(members, dict)
        self.assertEquals(3, len(members))
        self.assertEquals(3, len(self.members))
        self.assertIsInstance(self.members[200], Member)
        self.assertIsInstance(self.members[201], Member)
        self.assertIsInstance(self.members[202], Member)
        self.assertEquals(self.members[200]['email'], u"test01@example.org")
        self.assertEquals(self.members[201]['email'], u"test02@example.org")
        self.assertEquals(self.members[202]['email'], u"test03@example.org")