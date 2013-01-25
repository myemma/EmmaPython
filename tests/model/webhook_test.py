import unittest
from emma import exceptions as ex
from emma.model.account import Account
from emma.model.webhook import WebHook
from tests.model import MockAdapter


class WebHookTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.webhook = WebHook(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'webhook_id':200,
                'url': u"http://example.com",
                'method': u"POST",
                'event': u"mailing_finish"
            }
        )

    def test_can_delete_a_webhook(self):
        del(self.webhook['webhook_id'])

        with self.assertRaises(ex.NoWebHookIdError):
            self.webhook.delete()
        self.assertEquals(self.webhook.account.adapter.called, 0)

    def test_can_delete_a_webhook2(self):
        MockAdapter.expected = True

        result = self.webhook.delete()

        self.assertIsNone(result)
        self.assertEquals(self.webhook.account.adapter.called, 1)
        self.assertEquals(
            self.webhook.account.adapter.call,
            ('DELETE', '/webhooks/200', {}))

    def test_can_save_a_webhook(self):
        del(self.webhook['webhook_id'])
        MockAdapter.expected = 1024

        result = self.webhook.save()

        self.assertIsNone(result)
        self.assertEquals(self.webhook.account.adapter.called, 1)
        self.assertEquals(
            self.webhook.account.adapter.call,
            (
                'POST',
                '/webhooks',
                {
                    'url': u"http://example.com",
                    'method': u"POST",
                    'event': u"mailing_finish"
                }))
        self.assertEquals(1024, self.webhook['webhook_id'])

    def test_can_save_a_webhook2(self):
        MockAdapter.expected = True

        self.webhook['url'] = u"http://v2.example.com"
        result = self.webhook.save()

        self.assertIsNone(result)
        self.assertEquals(self.webhook.account.adapter.called, 1)
        self.assertEquals(
            self.webhook.account.adapter.call,
            (
                'PUT',
                '/webhooks/200',
                {
                    'url': u"http://v2.example.com",
                    'method': u"POST",
                    'event': u"mailing_finish"
                }))
