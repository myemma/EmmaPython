"""Audience mailing models"""

from datetime import datetime
from emma import exceptions as ex
from emma.enumerations import MailingStatus
from emma.model import BaseApiModel, str_fields_to_datetime
import emma.model.group
import emma.model.member
import emma.model.search
import emma.model.message


class Mailing(BaseApiModel):
    """
    Encapsulates operations for a :class:`Mailing`

    :param account: The Account which owns this Mailing
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Mailing`
    :type raw: :class:`dict`

    Usage::

        >>> from emma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> mlng = acct.mailings[123]
        >>> mlng
        <Mailing>
    """
    def __init__(self, account, raw=None):
        self.account = account
        super(Mailing, self).__init__(raw)
        self.groups = MailingGroupCollection(self)
        self.members = MailingMemberCollection(self)
        self.messages = MailingMessageCollection(self)
        self.searches = MailingSearchCollection(self)

    def _parse_raw(self, raw):
        raw.update(str_fields_to_datetime(
            ['clicked', 'opened', 'delivery_ts', 'forwarded', 'shared', 'sent',
             'send_finished', 'send_at', 'archived_ts', 'send_started',
             'started_or_finished'],
            raw))
        return raw

    def update_status(self, status):
        """
        Update status of a current mailing.

        :param status: The new mailing status
        :type status: :class:`str`
        :rtype: :class:`None`

        Usage::

            >>> from emma.model.account import Account
            >>> from emma.enumerations import MailingStatus
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.update_statues(MailingStatus.Canceled)
            None
            >>> mlng.update_statues(MailingStatus.Ready)
            <MailingStatusUpdateError>
        """
        if 'mailing_id' not in self._dict:
            raise ex.NoMailingIdError()

        path = "/mailings/%s" % self._dict['mailing_id']
        data = {'status': {
            MailingStatus.Canceled: "canceled",
            MailingStatus.Paused: "paused",
            MailingStatus.Ready: "ready"
        }[status]}
        self._dict['status'] = self.account.adapter.put(path, data)

    def is_archived(self):
        """
        Whether a mailing has been archived

        :rtype: :class:`bool`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.is_archived()
            False
            >>> mlng.archive()
            >>> mlng.is_archived()
            True
        """
        return 'archived_ts' in self._dict and bool(self._dict['archived_ts'])

    def archive(self):
        """
        Sets archived timestamp for a mailing.

        :rtype: :class:`None`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.archive()
            None
        """
        if 'mailing_id' not in self._dict:
            raise ex.NoMailingIdError()
        if self.is_archived():
            return None

        path = "/mailings/%s" % self._dict['mailing_id']
        if not self.account.adapter.delete(path):
            raise ex.MailingArchiveError()

        self._dict['archived_ts'] = datetime.now()

    def cancel(self):
        """
        Cancels a mailing that has a current status of pending or paused.

        :rtype: :class:`None`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.cancel()
            None
        """
        if 'mailing_id' not in self._dict:
            raise ex.NoMailingIdError()

        path = "/mailings/cancel/%s" % self._dict['mailing_id']
        if not self.account.adapter.delete(path):
            raise ex.MailingCancelError()

    def send_additional(self, recipient_emails=None, sender=None,
                        heads_up_emails=None, recipient_groups=None,
                        recipient_searches=None):
        """
        Send a prior mailing to additional recipients. A new mailing will be
        created that inherits its content from the original.

        :param recipient_emails: The additional emails to which this mailing shall be sent
        :type recipient_emails: :class:`list` of :class:`str`
        :rtype: :class:`int`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.send_additional(["test2@example.com"])
            124
        """
        if 'mailing_id' not in self._dict:
            raise ex.NoMailingIdError()

        path = "/mailings/%s" % self._dict['mailing_id']
        data = dict(x for x in {
            'recipient_emails': recipient_emails,
            'sender': sender,
            'heads_up_emails': heads_up_emails,
            'recipient_groups': recipient_groups,
            'recipient_searches': recipient_searches
        }.items() if x[1] is not None)

        if not data:
            return None

        result = self.account.adapter.post(path, data)

        if result:
            return result['mailing_id']

    def get_heads_up_emails(self):
        """
        Get heads up email address(es) related to a mailing.

        :rtype: :class:`list` of :class:`str`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.get_heads_up_emails()
            ["headsup1@example.com", "headsup2@example.com"]
        """
        if 'mailing_id' not in self._dict:
            raise ex.NoMailingIdError()

        path = "/mailings/%s/headsup" % self._dict['mailing_id']

        return self.account.adapter.get(path)

    def force_split_test_winner(self, winner_id):
        """
        Declare the winner of a split test manually. In the event that the test
        duration has not elapsed, the current stats for each test will be frozen
        and the content defined in the user declared winner will sent to the
        remaining members for the mailing. Please note, any messages that are
        pending for each of the test variations will receive the content
        assigned to them when the test was initially constructed.

        :param winner_id: The identifier for the winner
        :type winner_id: :class:`int`
        :rtype: :class:`None`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.winner(12)
            None
        """
        if 'mailing_id' not in self._dict:
            raise ex.NoMailingIdError()

        path = "/mailings/%s/winner/%s" % (self._dict['mailing_id'], winner_id)

        self.account.adapter.post(path)


class MailingGroupCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Group` objects of a
    :class:`Mailing`

    :param mailing: The Mailing which owns this collection
    :type mailing: :class:`Mailing`
    """
    def __init__(self, mailing):
        self.mailing = mailing
        super(MailingGroupCollection, self).__init__()

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Group` objects

        :rtype: :class:`dict` of :class:`Group` objects

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.groups.fetch_all()
            {123: <Group>, 321: <Group>, ...}

        """
        if 'mailing_id' not in self.mailing:
            raise ex.NoMailingIdError()
        group = emma.model.group
        path = '/mailings/%s/groups' % self.mailing['mailing_id']
        if not self._dict:
            self._dict = dict(
                (x['group_id'], group.Group(self.mailing.account, x))
                    for x in self.mailing.account.adapter.paginated_get(path))
        return self._dict


class MailingMemberCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Member` objects of a
    :class:`Mailing`

    :param mailing: The Mailing which owns this collection
    :type mailing: :class:`Mailing`
    """
    def __init__(self, mailing):
        self.mailing = mailing
        super(MailingMemberCollection, self).__init__()

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Member` objects

        :rtype: :class:`dict` of :class:`Member` objects

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.members.fetch_all()
            {123: <Member>, 321: <Member>, ...}

        """
        if 'mailing_id' not in self.mailing:
            raise ex.NoMailingIdError()
        member = emma.model.member
        path = '/mailings/%s/members' % self.mailing['mailing_id']
        if not self._dict:
            self._dict = dict(
                (x['member_id'], member.Member(self.mailing.account, x))
                    for x in self.mailing.account.adapter.paginated_get(path))
        return self._dict


class MailingSearchCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Search` objects of a
    :class:`Mailing`

    :param mailing: The Mailing which owns this collection
    :type mailing: :class:`Mailing`
    """
    def __init__(self, mailing):
        self.mailing = mailing
        super(MailingSearchCollection, self).__init__()

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Search` objects

        :rtype: :class:`dict` of :class:`Search` objects

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.searches.fetch_all()
            {123: <Search>, 321: <Search>, ...}

        """
        if 'mailing_id' not in self.mailing:
            raise ex.NoMailingIdError()
        search = emma.model.search
        path = '/mailings/%s/searches' % self.mailing['mailing_id']
        if not self._dict:
            self._dict = dict(
                (x['search_id'], search.Search(self.mailing.account, x))
                    for x in self.mailing.account.adapter.paginated_get(path))
        return self._dict


class MailingMessageCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Message` objects of a
    :class:`Mailing`

    :param mailing: The Mailing which owns this collection
    :type mailing: :class:`Mailing`
    """
    def __init__(self, mailing):
        self.mailing = mailing
        super(MailingMessageCollection, self).__init__()

    def __getitem__(self, key):
        item = self.find_one_by_member_id(key)
        if not item:
            raise KeyError(key)
        return item

    def find_one_by_member_id(self, member_id, message_type=None):
        """
        Lazy-loads a single :class:`Message` by Member ID

        :param member_id: The member identifier
        :type member_id: :class:`int`
        :param message_type: The portion of the message to retrieve
        :type message_type: :class:`str`
        :rtype: :class:`dict` or :class:`None`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.messages(12)
            {'plaintext': ..., 'subject': ..., 'html_body': ...}
            >>> from emma.enumerations import PersonalizedMessageType as pmt
            >>> mlng.messages(12, type=pmt.Html)
            {'html_body': ...}
        """
        if 'mailing_id' not in self.mailing:
            raise ex.NoMailingIdError()

        member_id = int(member_id)
        path = "/mailings/%s/messages/%s" % (
            self.mailing['mailing_id'], member_id)
        params = {'type': message_type} if message_type else {}
        if member_id not in self._dict:
            message = emma.model.message
            raw = self.mailing.account.adapter.get(path, params)
            if raw:
                self._dict[member_id] = message.Message(
                    self.mailing, member_id, raw)

        return (member_id in self._dict) and self._dict[member_id] or None
