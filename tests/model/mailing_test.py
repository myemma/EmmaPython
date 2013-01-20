from datetime import datetime
import unittest
from myemma.model.account import Account
from myemma.model.mailing import Mailing
from myemma.model import SERIALIZED_DATETIME_FORMAT
from tests.model import MockAdapter


class GroupTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.group = Mailing(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'mailing_id': 200,
                'delivery_ts': datetime.now().strftime(SERIALIZED_DATETIME_FORMAT),
                'clicked': None,
                'opened': None,
                'forwarded': None,
                'shared': None,
                'sent':  datetime.now().strftime(SERIALIZED_DATETIME_FORMAT)
            }
        )

    def test_can_parse_special_fields_correctly(self):
        self.assertIsInstance(self.group['delivery_ts'], datetime)
        self.assertIsInstance(self.group['sent'], datetime)
        self.assertIsNone(self.group['clicked'])
        self.assertIsNone(self.group['opened'])
        self.assertIsNone(self.group['forwarded'])
        self.assertIsNone(self.group['shared'])
