from datetime import datetime
import unittest
from myemma import exceptions as ex
from myemma.model.account import Account
from myemma.model.search import Search
from myemma.model import SERIALIZED_DATETIME_FORMAT
from tests.model import MockAdapter


class FieldTest(unittest.TestCase):
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

    def test_can_delete_a_field(self):
        del(self.search['search_id'])

        with self.assertRaises(ex.NoSearchIdError):
            self.search.delete()
        self.assertEquals(self.search.account.adapter.called, 0)
        self.assertFalse(self.search.is_deleted())

    def test_can_delete_a_field2(self):
        self.search['deleted_at'] = datetime.now()

        result = self.search.delete()

        self.assertIsNone(result)
        self.assertEquals(self.search.account.adapter.called, 0)
        self.assertTrue(self.search.is_deleted())

    def test_can_delete_a_field3(self):
        MockAdapter.expected = True

        result = self.search.delete()

        self.assertIsNone(result)
        self.assertEquals(self.search.account.adapter.called, 1)
        self.assertEquals(
            self.search.account.adapter.call,
            ('DELETE', '/searches/200', {}))
        self.assertTrue(self.search.is_deleted())
