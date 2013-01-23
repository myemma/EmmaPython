from datetime import datetime
import unittest
from myemma import exceptions as ex
from myemma.enumerations import PersonalizedMessageType as pmt, MailingStatus
from myemma.model.account import Account
from myemma.model.mailing import (Mailing, MailingMemberCollection, MailingGroupCollection, MailingSearchCollection)
from myemma.model.member import Member
from myemma.model.group import Group
from myemma.model.search import Search
from myemma.model.message import Message
from myemma.model import SERIALIZED_DATETIME_FORMAT
from tests.model import MockAdapter


class MailingTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.mailing = Mailing(
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
        self.assertIsInstance(self.mailing['delivery_ts'], datetime)
        self.assertIsInstance(self.mailing['sent'], datetime)
        self.assertIsNone(self.mailing['clicked'])
        self.assertIsNone(self.mailing['opened'])
        self.assertIsNone(self.mailing['forwarded'])
        self.assertIsNone(self.mailing['shared'])

    def test_can_update_the_status_of_a_mailing(self):
        with self.assertRaises(KeyError):
            self.mailing.update_status(MailingStatus.Failed)
        self.assertEquals(self.mailing.account.adapter.called, 0)

    def test_can_update_the_status_of_a_mailing2(self):
        del(self.mailing['mailing_id'])

        with self.assertRaises(ex.NoMailingIdError):
            self.mailing.update_status(MailingStatus.Failed)
        self.assertEquals(self.mailing.account.adapter.called, 0)

    def test_can_update_the_status_of_a_mailing3(self):
        MockAdapter.expected = MailingStatus.Paused
        result = self.mailing.update_status(MailingStatus.Paused)
        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('PUT', '/mailings/200', {'status':"paused"}))
        self.assertIsNone(result)
        self.assertEquals(self.mailing['status'], MailingStatus.Paused)

    def test_can_archive_a_mailing(self):
        MockAdapter.expected = False
        with self.assertRaises(ex.MailingArchiveError):
            self.mailing.archive()
        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('DELETE', '/mailings/200', {}))

    def test_can_archive_a_mailing2(self):
        MockAdapter.expected = True
        result = self.mailing.archive()
        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('DELETE', '/mailings/200', {}))
        self.assertIsNone(result)

    def test_can_archive_a_mailing3(self):
        del(self.mailing['mailing_id'])
        with self.assertRaises(ex.NoMailingIdError):
            self.mailing.archive()
        self.assertEquals(self.mailing.account.adapter.called, 0)

    def test_can_archive_a_mailing4(self):
        self.mailing['archived_ts'] = datetime.now()
        result = self.mailing.archive()
        self.assertIsNone(result)
        self.assertEquals(self.mailing.account.adapter.called, 0)

    def test_can_cancel_a_mailing(self):
        MockAdapter.expected = False
        with self.assertRaises(ex.MailingCancelError):
            self.mailing.cancel()
        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('DELETE', '/mailings/cancel/200', {}))

    def test_can_cancel_a_mailing2(self):
        MockAdapter.expected = True
        result = self.mailing.cancel()
        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('DELETE', '/mailings/cancel/200', {}))
        self.assertIsNone(result)

    def test_can_cancel_a_mailing3(self):
        del(self.mailing['mailing_id'])
        with self.assertRaises(ex.NoMailingIdError):
            self.mailing.cancel()
        self.assertEquals(self.mailing.account.adapter.called, 0)

    def test_can_send_mailing_to_additional_targets(self):
        # Setup
        MockAdapter.expected = {'mailing_id': 201}

        mailing_id = self.mailing.send_additional(["test2@example.com"])

        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            (
                'POST',
                '/mailings/200',
                {
                    "recipient_emails": ["test2@example.com"]
                }))
        self.assertEquals(201, mailing_id)

    def test_can_send_mailing_to_additional_targets2(self):
        # Setup
        MockAdapter.expected = None

        mailing_id = self.mailing.send_additional(["test2@example.com"])

        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            (
                'POST',
                '/mailings/200',
                {
                    "recipient_emails": ["test2@example.com"]
                }))
        self.assertIsNone(mailing_id)

    def test_can_send_mailing_to_additional_targets3(self):
        # Setup
        MockAdapter.expected = None

        mailing_id = self.mailing.send_additional(
            ["test2@example.com"],
            "sender@example.com",
            ["heads_up@example.com"],
            [300, 301],
            [400, 401]
        )

        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            (
                'POST',
                '/mailings/200',
                {
                    "recipient_emails": ["test2@example.com"],
                    "sender": "sender@example.com",
                    "heads_up_emails": ["heads_up@example.com"],
                    "recipient_groups": [300, 301],
                    "recipient_searches": [400, 401]
                }))
        self.assertIsNone(mailing_id)

    def test_can_send_mailing_to_additional_targets4(self):
        # Setup
        MockAdapter.expected = None

        mailing_id = self.mailing.send_additional(
            recipient_emails=["test2@example.com"],
            sender="sender@example.com",
            heads_up_emails=["heads_up@example.com"],
            recipient_groups=[300, 301],
            recipient_searches=[400, 401]
        )

        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            (
                'POST',
                '/mailings/200',
                {
                    "recipient_emails": ["test2@example.com"],
                    "sender": "sender@example.com",
                    "heads_up_emails": ["heads_up@example.com"],
                    "recipient_groups": [300, 301],
                    "recipient_searches": [400, 401]
                }))
        self.assertIsNone(mailing_id)

    def test_can_send_mailing_to_additional_targets5(self):
        del(self.mailing['mailing_id'])

        with self.assertRaises(ex.NoMailingIdError):
            self.mailing.send_additional(["test2@example.com"])

        self.assertEquals(self.mailing.account.adapter.called, 0)

    def test_can_send_mailing_to_additional_targets6(self):
        mailing_id = self.mailing.send_additional()

        self.assertEquals(self.mailing.account.adapter.called, 0)
        self.assertIsNone(mailing_id)

    def test_can_get_heads_up_emails(self):
        del(self.mailing['mailing_id'])

        with self.assertRaises(ex.NoMailingIdError):
            self.mailing.get_heads_up_emails()
        self.assertEquals(self.mailing.account.adapter.called, 0)

    def test_can_get_heads_up_emails2(self):
        MockAdapter.expected = None

        emails = self.mailing.get_heads_up_emails()

        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('GET', '/mailings/200/headsup', {}))
        self.assertIsNone(emails)

    def test_can_get_heads_up_emails3(self):
        MockAdapter.expected = []

        emails = self.mailing.get_heads_up_emails()

        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('GET', '/mailings/200/headsup', {}))
        self.assertIsInstance(emails, list)

    def test_can_get_heads_up_emails4(self):
        MockAdapter.expected = ["headsup0@example.com", "headsup1@example.com"]

        emails = self.mailing.get_heads_up_emails()

        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('GET', '/mailings/200/headsup', {}))
        self.assertIsInstance(emails, list)
        self.assertEquals(2, len(emails))
        self.assertEquals("headsup0@example.com", emails[0])
        self.assertEquals("headsup1@example.com", emails[1])

    def test_can_force_split_test_winner(self):
        # Setup
        MockAdapter.expected = True

        result = self.mailing.force_split_test_winner(1024)

        self.assertEquals(self.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.mailing.account.adapter.call,
            ('POST', '/mailings/200/winner/1024', {}))
        self.assertIsNone(result)

    def test_can_force_split_test_winner2(self):
        del(self.mailing['mailing_id'])

        with self.assertRaises(ex.NoMailingIdError):
            self.mailing.force_split_test_winner(1024)
        self.assertEquals(self.mailing.account.adapter.called, 0)


class MailingGroupCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.groups =  Mailing(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {'mailing_id':200}
        ).groups

    def test_fetch_all_returns_a_dictionary(self):
        mailing = Mailing(self.groups.mailing.account)
        groups = MailingGroupCollection(mailing)
        with self.assertRaises(ex.NoMailingIdError):
            groups.fetch_all()
        self.assertEquals(groups.mailing.account.adapter.called, 0)

    def test_fetch_all_returns_a_dictionary2(self):
        MockAdapter.expected = [{'group_id':1024, 'group_name':u"Test Group"}]
        self.assertIsInstance(self.groups.fetch_all(), dict)
        self.assertEquals(self.groups.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.groups.mailing.account.adapter.call,
            ('GET', '/mailings/200/groups', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{'group_id':1024, 'group_name':u"Test Group"}]
        self.assertEquals(0, len(self.groups))
        self.groups.fetch_all()
        self.assertEquals(1, len(self.groups))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{'group_id':1024, 'group_name':u"Test Group"}]
        self.groups.fetch_all()
        self.groups.fetch_all()
        self.assertEquals(self.groups.mailing.account.adapter.called, 1)

    def test_collection_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{'group_id':1024, 'group_name':u"Test Group"}]
        self.groups.fetch_all()
        self.assertIsInstance(self.groups, MailingGroupCollection)
        self.assertEquals(1, len(self.groups))
        self.assertIsInstance(self.groups[1024], Group)
        self.assertEquals(self.groups[1024]['group_id'], 1024)
        self.assertEquals(self.groups[1024]['group_name'], u"Test Group")


class MailingMemberCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.members =  Mailing(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {'mailing_id':200}
        ).members

    def test_fetch_all_returns_a_dictionary(self):
        mailing = Mailing(self.members.mailing.account)
        members = MailingMemberCollection(mailing)
        with self.assertRaises(ex.NoMailingIdError):
            members.fetch_all()
        self.assertEquals(members.mailing.account.adapter.called, 0)

    def test_fetch_all_returns_a_dictionary2(self):
        MockAdapter.expected = [{'member_id':1024, 'email':u"test@example.com"}]
        self.assertIsInstance(self.members.fetch_all(), dict)
        self.assertEquals(self.members.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.members.mailing.account.adapter.call,
            ('GET', '/mailings/200/members', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{'member_id':1024, 'email':u"test@example.com"}]
        self.assertEquals(0, len(self.members))
        self.members.fetch_all()
        self.assertEquals(1, len(self.members))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{'member_id':1024, 'email':u"test@example.com"}]
        self.members.fetch_all()
        self.members.fetch_all()
        self.assertEquals(self.members.mailing.account.adapter.called, 1)

    def test_collection_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{'member_id':1024, 'email':u"test@example.com"}]
        self.members.fetch_all()
        self.assertIsInstance(self.members, MailingMemberCollection)
        self.assertEquals(1, len(self.members))
        self.assertIsInstance(self.members[1024], Member)
        self.assertEquals(self.members[1024]['member_id'], 1024)
        self.assertEquals(self.members[1024]['email'], u"test@example.com")


class MailingSearchCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.searches =  Mailing(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {'mailing_id':200}
        ).searches

    def test_fetch_all_returns_a_dictionary(self):
        del(self.searches.mailing['mailing_id'])
        with self.assertRaises(ex.NoMailingIdError):
            self.searches.fetch_all()
        self.assertEquals(self.searches.mailing.account.adapter.called, 0)

    def test_fetch_all_returns_a_dictionary2(self):
        MockAdapter.expected = [{'search_id':1024}]
        self.assertIsInstance(self.searches.fetch_all(), dict)
        self.assertEquals(self.searches.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.searches.mailing.account.adapter.call,
            ('GET', '/mailings/200/searches', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{'search_id':1024}]
        self.assertEquals(0, len(self.searches))
        self.searches.fetch_all()
        self.assertEquals(1, len(self.searches))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{'search_id':1024}]
        self.searches.fetch_all()
        self.searches.fetch_all()
        self.assertEquals(self.searches.mailing.account.adapter.called, 1)

    def test_collection_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{'search_id':1024}]
        self.searches.fetch_all()
        self.assertIsInstance(self.searches, MailingSearchCollection)
        self.assertEquals(1, len(self.searches))
        self.assertIsInstance(self.searches[1024], Search)
        self.assertEquals(self.searches[1024]['search_id'], 1024)


class MailingMessageCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.messages =  Mailing(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {'mailing_id':200}
        ).messages

    def test_can_get_personalized_message_by_member_id(self):
        del(self.messages.mailing['mailing_id'])
        with self.assertRaises(ex.NoMailingIdError):
            self.messages.find_one_by_member_id(1024)
        self.assertEquals(self.messages.mailing.account.adapter.called, 0)

    def test_can_get_personalized_message_by_member_id2(self):
        MockAdapter.expected = {'subject': "Test Subject"}
        result = self.messages.find_one_by_member_id(1024)
        self.assertEquals(self.messages.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.messages.mailing.account.adapter.call,
            ('GET', '/mailings/200/messages/1024', {}))
        self.assertIsInstance(result, Message)

    def test_can_get_personalized_message_by_member_id3(self):
        MockAdapter.expected = {'subject': "Test Subject"}
        result = self.messages.find_one_by_member_id(1024, pmt.Html)
        self.assertEquals(self.messages.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.messages.mailing.account.adapter.call,
            ('GET', '/mailings/200/messages/1024', {'type':"html"}))
        self.assertIsInstance(result, Message)

    def test_can_get_personalized_message_by_member_id4(self):
        MockAdapter.expected = {'subject': "Test Subject"}
        result = self.messages.find_one_by_member_id(1024, pmt.PlainText)
        self.assertEquals(self.messages.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.messages.mailing.account.adapter.call,
            ('GET', '/mailings/200/messages/1024', {'type':"plaintext"}))
        self.assertIsInstance(result, Message)

    def test_can_get_personalized_message_by_member_id5(self):
        MockAdapter.expected = {'subject': "Test Subject"}
        result = self.messages.find_one_by_member_id(1024, pmt.Subject)
        self.assertEquals(self.messages.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.messages.mailing.account.adapter.call,
            ('GET', '/mailings/200/messages/1024', {'type':"subject"}))
        self.assertIsInstance(result, Message)

    def test_find_one_by_member_id_populates_collection(self):
        # Setup
        MockAdapter.expected = {'subject': "Test Subject"}

        self.messages.find_one_by_member_id(1024)

        self.assertIn(1024, self.messages)
        self.assertIsInstance(self.messages[1024], Message)

    def test_find_one_by_member_id_caches_result(self):
        # Setup
        MockAdapter.expected = {'subject': "Test Subject"}

        self.messages.find_one_by_member_id(1024)
        self.messages.find_one_by_member_id(1024)

        self.assertEquals(self.messages.mailing.account.adapter.called, 1)

    def test_dictionary_access_lazy_loads_by_member_id(self):
        # Setup
        MockAdapter.expected = {'subject': "Test Subject"}

        message = self.messages[1024]

        self.assertIn(1024, self.messages)
        self.assertIsInstance(message, Message)
        self.assertEquals(self.messages.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.messages.mailing.account.adapter.call,
            ('GET', '/mailings/200/messages/1024', {}))

    def test_dictionary_access_lazy_loads_by_member_id2(self):
        # Setup
        MockAdapter.expected = None

        message = self.messages[1024]

        self.assertEquals(0, len(self.messages))
        self.assertIsNone(message)
        self.assertEquals(self.messages.mailing.account.adapter.called, 1)
        self.assertEquals(
            self.messages.mailing.account.adapter.call,
            ('GET', '/mailings/200/messages/1024', {}))
