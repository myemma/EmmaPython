from datetime import datetime
import unittest
from myemma import exceptions as ex
from myemma.model.account import Account
from myemma.model.field import Field
from myemma.model import SERIALIZED_DATETIME_FORMAT
from tests.model import MockAdapter


class FieldTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.field = Field(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'shortcut_name': u"test_field"
            }
        )

    def test_can_delete_a_field(self):
        fld = Field(self.field.account)

        with self.assertRaises(ex.NoFieldIdError):
            fld.delete()
        self.assertEquals(self.field.account.adapter.called, 0)
        self.assertFalse(self.field.is_deleted())

    def test_can_delete_a_field2(self):
        MockAdapter.expected = None
        fld = Field(
            self.field.account,
            {
                'field_id': 200,
                'deleted_at': datetime.now().strftime(SERIALIZED_DATETIME_FORMAT)
            })

        result = fld.delete()

        self.assertIsNone(result)
        self.assertEquals(fld.account.adapter.called, 0)
        self.assertTrue(fld.is_deleted())

    def test_can_delete_a_field3(self):
        MockAdapter.expected = True
        fld = Field(
            self.field.account,
            {
                'field_id': 200,
                'deleted_at': None
            })

        result = fld.delete()

        self.assertIsNone(result)
        self.assertEquals(fld.account.adapter.called, 1)
        self.assertEquals(
            fld.account.adapter.call,
            ('DELETE', '/fields/200', {}))
        self.assertTrue(fld.is_deleted())
