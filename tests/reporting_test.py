import unittest
from emma.model.account import Account
from emma.enumerations import Report, DeliveryType
from emma import get_report
from tests.model import MockAdapter


class ReportingTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.account = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy")

    def test_can_get_response_summary(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.ResponseSummary)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response', {}))

    def test_can_get_response_summary2(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.ResponseSummary, params={'include_archived': True})
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response', {'include_archived': True}))

    def test_can_get_response_summary3(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.ResponseSummary, params={'range': "2011-04-01~2011-09-01"})
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response', {'range': "2011-04-01~2011-09-01"}))

    def test_can_get_response_summary_for_mailing(self):
        MockAdapter.expected = {}
        report = get_report(self.account, Report.MailingSummary, 123)
        self.assertIsInstance(report, dict)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123', {}))

    def test_can_get_sent_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.SentList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/sends', {}))

    def test_can_get_in_progress_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.InProgressList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/in_progress', {}))

    def test_can_get_deliveries_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.DeliveredList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/deliveries', {}))

    def test_can_get_deliveries_list_for_mailing2(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.DeliveredList, 123, {'del_status': DeliveryType.Delivered})
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/deliveries', {'del_status': 'd'}))

    def test_can_get_opens_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.OpenList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/opens', {}))

    def test_can_get_links_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.LinkList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/links', {}))

    def test_can_get_clicks_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.ClickList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/clicks', {}))

    def test_can_get_clicks_list_for_mailing2(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.ClickList, 123, {'member_id': 1024})
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/clicks', {'member_id': 1024}))

    def test_can_get_clicks_list_for_mailing3(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.ClickList, 123, {'link_id': 1024})
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/clicks', {'link_id': 1024}))

    def test_can_get_forwards_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.ForwardList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/forwards', {}))

    def test_can_get_optouts_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.OptOutList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/optouts', {}))

    def test_can_get_signups_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.SignUpList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/signups', {}))

    def test_can_get_shares_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.SharesList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/shares', {}))

    def test_can_get_customer_shares_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.CustomerSharesList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/customer_shares', {}))

    def test_can_get_customer_share_clicks_list_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.CustomerShareClicksList, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/customer_share_clicks', {}))

    def test_can_get_customer_share_for_mailing(self):
        MockAdapter.expected = {}
        report = get_report(self.account, Report.CustomerShare, 123)
        self.assertIsInstance(report, dict)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/customer_share', {}))

    def test_can_get_shares_overview_for_mailing(self):
        MockAdapter.expected = []
        report = get_report(self.account, Report.SharesOverview, 123)
        self.assertIsInstance(report, list)
        self.assertEquals(self.account.adapter.called, 1)
        self.assertEquals(
            self.account.adapter.call,
            ('GET', '/response/123/shares/overview', {}))