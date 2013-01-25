"""Emma API Wrapper for Python"""
from enumerations import Report as r

def get_report(account, report, id=None, params=None):
    """
    Gets a response report for the given report

    :param account: The account for which these reports apply
    :type account: :class:`Account`
    :param report: The report (from enumerations.Report)
    :type report: :class:`int`
    :param id: An id such as mailing_id or share_id, if the report needs one
    :type id: :class:`int`
    :param params: Optional parameters to pass
    :type params: :class:`dict`
    :rtype: :class:`dict`

    Usage::

        >>> from emma import get_report
        >>> from emma.model.account import Account
        >>> from emma.enumerations import Report
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> get_report(acct, Report.ResponseSummary)
        [...]
        >>> get_report(acct, Report.ResponseSummary, None, {'include_archived': True})
        [...]
        >>> get_report(acct, Report.MailingSummary, 123)
        {...}
        >>> get_report(acct, Report.SentList, 123)
        [...]
    """
    params = params if params else {}
    path = {
        r.ResponseSummary: "/response",
        r.MailingSummary: "/response/%s" % id,
        r.SentList: "/response/%s/sends" % id,
        r.InProgressList: "/response/%s/in_progress" % id,
        r.DeliveredList: "/response/%s/deliveries" % id,
        r.OpenList: "/response/%s/opens" % id,
        r.LinkList: "/response/%s/links" % id,
        r.ClickList: "/response/%s/clicks" % id,
        r.ForwardList: "/response/%s/forwards" % id,
        r.OptOutList: "/response/%s/optouts" % id,
        r.SignUpList: "/response/%s/signups" % id,
        r.SharesList: "/response/%s/shares" % id,
        r.CustomerSharesList: "/response/%s/customer_shares" % id,
        r.CustomerShareClicksList: "/response/%s/customer_share_clicks" % id,
        r.CustomerShare: "/response/%s/customer_share" % id,
        r.SharesOverview: "/response/%s/shares/overview" % id,
    }[report]
    return account.adapter.get(path, params)