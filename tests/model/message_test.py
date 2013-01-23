import unittest
from myemma import exceptions as ex
from myemma.model.account import Account
from myemma.model.mailing import Mailing
from myemma.model.message import Message
from tests.model import MockAdapter


class MessageTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.message = Message(
            Mailing(
                Account(account_id="100", public_key="xxx", private_key="yyy"),
                {'mailing_id': 200}
            ),
            1024
        )

    def test_can_forward_a_message(self):
        MockAdapter.expected = False
        with self.assertRaises(ex.MailingForwardError):
            self.message.forward(["test@example.com"])
        self.assertEquals(self.message.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.message.mailing.account.adapter.call,
            ('POST', '/forwards/200/1024', {'recipient_emails':["test@example.com"]}))

    def test_can_forward_a_message2(self):
        MockAdapter.expected = {'mailing_id': 2048}
        mailing_id = self.message.forward(["test@example.com"])
        self.assertEquals(self.message.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.message.mailing.account.adapter.call,
            (
                'POST',
                '/forwards/200/1024',
                {'recipient_emails':["test@example.com"]}))
        self.assertIsInstance(mailing_id, int)
        self.assertEquals(mailing_id, 2048)

    def test_can_forward_a_message3(self):
        del(self.message.mailing['mailing_id'])
        with self.assertRaises(ex.NoMailingIdError):
            self.message.forward(["test@example.com"])
        self.assertEquals(self.message.mailing.account.adapter.called, 0)

    def test_can_forward_a_message4(self):
        self.message.member_id = None
        with self.assertRaises(ex.NoMemberIdError):
            self.message.forward(["test@example.com"])
        self.assertEquals(self.message.mailing.account.adapter.called, 0)

    def test_can_forward_a_message5(self):
        result = self.message.forward()
        self.assertEquals(self.message.mailing.account.adapter.called, 0)
        self.assertIsNone(result)

    def test_can_forward_a_message6(self):
        MockAdapter.expected = {'mailing_id': 2048}
        mailing_id = self.message.forward(["test@example.com"], "Test Note")
        self.assertEquals(self.message.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.message.mailing.account.adapter.call,
            (
                'POST',
                '/forwards/200/1024',
                {
                    'recipient_emails':["test@example.com"],
                    'note': "Test Note"
                }))
        self.assertIsInstance(mailing_id, int)
        self.assertEquals(mailing_id, 2048)
