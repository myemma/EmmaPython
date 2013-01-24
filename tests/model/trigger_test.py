from datetime import datetime
import unittest
from myemma import exceptions as ex
from myemma.model.account import Account
from myemma.model.trigger import Trigger
from myemma.model import SERIALIZED_DATETIME_FORMAT
from myemma.model.mailing import Mailing
from tests.model import MockAdapter


class SearchTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.trigger = Trigger(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'trigger_id':200,
                'start_ts': datetime.now().strftime(SERIALIZED_DATETIME_FORMAT),
                'deleted_at':None,
                'parent_mailing': {
                    'mailing_type': "m",
                    'send_started': None,
                    'signup_form_id': None,
                    'mailing_id': 1024,
                    'plaintext': "Hello [% member:first_name %]!",
                    'recipient_count': 0,
                    'year': None,
                    'account_id': 100,
                    'month': None,
                    'disabled': False,
                    'parent_mailing_id': None,
                    'started_or_finished': None,
                    'name': "Sample Mailing",
                    'mailing_status': "c",
                    'plaintext_only': False,
                    'sender': "Test Sender",
                    'send_finished': None,
                    'send_at': None,
                    'reply_to': None,
                    'subject': "Parent Mailing",
                    'archived_ts': None,
                    'html_body': "<p>Hello [% member:first_name %]!</p>"
                }
            }
        )

    def test_can_parse_special_fields_correctly(self):
        self.assertIsInstance(self.trigger['start_ts'], datetime)
        self.assertIsInstance(self.trigger['parent_mailing'], Mailing)
        self.assertIsNone(self.trigger['deleted_at'])

    def test_can_delete_a_trigger(self):
        del(self.trigger['trigger_id'])

        with self.assertRaises(ex.NoTriggerIdError):
            self.trigger.delete()
        self.assertEquals(self.trigger.account.adapter.called, 0)
        self.assertFalse(self.trigger.is_deleted())

    def test_can_delete_a_trigger2(self):
        self.trigger['deleted_at'] = datetime.now()

        result = self.trigger.delete()

        self.assertIsNone(result)
        self.assertEquals(self.trigger.account.adapter.called, 0)
        self.assertTrue(self.trigger.is_deleted())

    def test_can_delete_a_trigger3(self):
        MockAdapter.expected = True

        result = self.trigger.delete()

        self.assertIsNone(result)
        self.assertEquals(self.trigger.account.adapter.called, 1)
        self.assertEquals(
            self.trigger.account.adapter.call,
            ('DELETE', '/triggers/200', {}))
        self.assertTrue(self.trigger.is_deleted())

    def test_can_save_a_trigger(self):
        trigger = Trigger(
            self.trigger.account,
            {'name':u"Test Trigger"}
        )
        MockAdapter.expected = 1024

        result = trigger.save()

        self.assertIsNone(result)
        self.assertEquals(trigger.account.adapter.called, 1)
        self.assertEquals(
            trigger.account.adapter.call,
            (
                'POST',
                '/triggers',
                {
                    'name': u"Test Trigger"
                }))
        self.assertEquals(1024, trigger['trigger_id'])

    def test_can_save_a_trigger2(self):
        MockAdapter.expected = True

        self.trigger['name'] = u"Renamed Trigger"
        result = self.trigger.save()

        self.assertIsNone(result)
        self.assertEquals(self.trigger.account.adapter.called, 1)
        self.assertEquals(
            self.trigger.account.adapter.call,
            ('PUT', '/triggers/200',  {'name': u"Renamed Trigger"}))


class TriggerMailingCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.mailings = Trigger(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {'trigger_id': 1024}
        ).mailings

    def test_can_fetch_all_mailings(self):
        del(self.mailings.trigger['trigger_id'])
        with self.assertRaises(ex.NoSearchIdError):
            self.mailings.fetch_all()
        self.assertEquals(self.mailings.trigger.account.adapter.called, 0)

    def test_can_fetch_all_mailings2(self):
        # Setup
        MockAdapter.expected = [
            {'mailing_id': 200},
            {'mailing_id': 201},
            {'mailing_id': 202}
        ]

        mailings = self.mailings.fetch_all()

        self.assertEquals(self.mailings.trigger.account.adapter.called, 1)
        self.assertEquals(
            self.mailings.trigger.account.adapter.call,
            ('GET', '/triggers/1024/mailings', {}))
        self.assertIsInstance(mailings, dict)
        self.assertEquals(3, len(mailings))
        self.assertEquals(3, len(self.mailings))
        self.assertIsInstance(self.mailings[200], Mailing)
        self.assertIsInstance(self.mailings[201], Mailing)
        self.assertIsInstance(self.mailings[202], Mailing)
