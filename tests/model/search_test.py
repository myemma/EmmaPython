from datetime import datetime
import unittest
from myemma import exceptions as ex
from myemma.model.account import Account
from myemma.model.search import Search
from myemma.model import SERIALIZED_DATETIME_FORMAT
from myemma.model.member import Member
from tests.model import MockAdapter


class SearchTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.search = Search(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'search_id':200,
                'deleted_at':None,
                'last_run_at':datetime.now().strftime(SERIALIZED_DATETIME_FORMAT)
            }
        )

    def test_can_parse_special_fields_correctly(self):
        self.assertIsInstance(self.search['last_run_at'], datetime)
        self.assertIsNone(self.search['deleted_at'])

    def test_can_delete_a_search(self):
        del(self.search['search_id'])

        with self.assertRaises(ex.NoSearchIdError):
            self.search.delete()
        self.assertEquals(self.search.account.adapter.called, 0)
        self.assertFalse(self.search.is_deleted())

    def test_can_delete_a_search2(self):
        self.search['deleted_at'] = datetime.now()

        result = self.search.delete()

        self.assertIsNone(result)
        self.assertEquals(self.search.account.adapter.called, 0)
        self.assertTrue(self.search.is_deleted())

    def test_can_delete_a_search3(self):
        MockAdapter.expected = True

        result = self.search.delete()

        self.assertIsNone(result)
        self.assertEquals(self.search.account.adapter.called, 1)
        self.assertEquals(
            self.search.account.adapter.call,
            ('DELETE', '/searches/200', {}))
        self.assertTrue(self.search.is_deleted())

    def test_can_save_a_search(self):
        srch = Search(
            self.search.account,
            {'name':u"Test Search", 'criteria':["group", "eq", "Test Group"]}
        )
        MockAdapter.expected = 1024

        result = srch.save()

        self.assertIsNone(result)
        self.assertEquals(srch.account.adapter.called, 1)
        self.assertEquals(
            srch.account.adapter.call,
            (
                'POST',
                '/searches',
                {
                    'name': u"Test Search",
                    'criteria':["group", "eq", "Test Group"]
                }))
        self.assertEquals(1024, srch['search_id'])

    def test_can_save_a_search2(self):
        MockAdapter.expected = True

        self.search['name'] = u"Test Search"
        self.search['criteria'] = ["group", "eq", "Test Group"]
        result = self.search.save()

        self.assertIsNone(result)
        self.assertEquals(self.search.account.adapter.called, 1)
        self.assertEquals(self.search.account.adapter.call,
            (
                'PUT',
                '/searches/200',
                {
                    'name': u"Test Search",
                    'criteria':["group", "eq", "Test Group"]
                }))


class SearchMemberCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.members = Search(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {'search_id': 1024}
        ).members

    def test_can_fetch_all_members(self):
        del(self.members.search['search_id'])
        with self.assertRaises(ex.NoSearchIdError):
            self.members.fetch_all()
        self.assertEquals(self.members.search.account.adapter.called, 0)

    def test_can_fetch_all_members2(self):
        # Setup
        MockAdapter.expected = [
            {'member_id': 200, 'email': u"test01@example.org"},
            {'member_id': 201, 'email': u"test02@example.org"},
            {'member_id': 202, 'email': u"test03@example.org"}
        ]

        members = self.members.fetch_all()

        self.assertEquals(self.members.search.account.adapter.called, 1)
        self.assertEquals(
            self.members.search.account.adapter.call,
            ('GET', '/searches/1024/members', {}))
        self.assertIsInstance(members, dict)
        self.assertEquals(3, len(members))
        self.assertEquals(3, len(self.members))
        self.assertIsInstance(self.members[200], Member)
        self.assertIsInstance(self.members[201], Member)
        self.assertIsInstance(self.members[202], Member)
        self.assertEquals(self.members[200]['email'], u"test01@example.org")
        self.assertEquals(self.members[201]['email'], u"test02@example.org")
        self.assertEquals(self.members[202]['email'], u"test03@example.org")
