"""Audience mailing models"""

from datetime import datetime
from myemma import exceptions as ex
from myemma.enumerations import MailingStatus
from myemma.model import BaseApiModel, str_fields_to_datetime
import myemma.model.group
import myemma.model.member
import myemma.model.search


class Mailing(BaseApiModel):
    """
    Encapsulates operations for a :class:`Mailing`

    :param account: The Account which owns this Mailing
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Mailing`
    :type raw: :class:`dict`

    Usage::

        >>> from myemma.model.account import Account
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
        self.searches = MailingSearchCollection(self)

    def _parse_raw(self, raw):
        raw.update(str_fields_to_datetime(
            ['clicked', 'opened', 'delivery_ts', 'forwarded', 'shared', 'sent',
             'send_finished', 'send_at', 'archived_ts', 'send_started',
             'started_or_finished'],
            raw))
        return raw

    def get_message_by_member_id(self, member_id, type=None):
        """
        Gets the personalized message content as sent to a specific member as
        part of the specified mailing.

        :param member_id: The member identifier
        :type member_id: :class:`int`
        :param type: The portion of the message to retrieve
        :type type: :class:`str`
        :rtype: :class:`dict` or :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.get_message_by_member_id(12)
            {'plaintext': ..., 'subject': ..., 'html_body': ...}
            >>> from myemma.enumerations import PersonalizedMessageType as pmt
            >>> mlng.get_message_by_member_id(12, type=pmt.Html)
            {'html_body': ...}
        """
        if 'mailing_id' not in self._dict:
            raise ex.NoMailingIdError()

        path = "/mailings/%s/messages/%s" % (self._dict['mailing_id'], member_id)
        params = {'type': type} if type else {}
        return self.account.adapter.get(path, params)

    def update_status(self, status):
        """
        Update status of a current mailing.

        :param status: The new mailing status
        :type status: :class:`str`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> from myemma.enumerations import MailingStatus
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

            >>> from myemma.model.account import Account
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

            >>> from myemma.model.account import Account
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

            >>> from myemma.model.account import Account
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

    def __delitem__(self, key):
        pass

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Group` objects

        :rtype: :class:`dict` of :class:`Group` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.groups.fetch_all()
            {123: <Group>, 321: <Group>, ...}

        """
        if 'mailing_id' not in self.mailing:
            raise ex.NoMailingIdError()
        group = myemma.model.group
        path = '/mailings/%s/groups' % self.mailing['mailing_id']
        if not self._dict:
            self._dict = dict(
                (x['group_id'], group.Group(self.mailing.account, x))
                    for x in self.mailing.account.adapter.get(path))
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

    def __delitem__(self, key):
        pass

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Member` objects

        :rtype: :class:`dict` of :class:`Member` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.members.fetch_all()
            {123: <Member>, 321: <Member>, ...}

        """
        if 'mailing_id' not in self.mailing:
            raise ex.NoMailingIdError()
        member = myemma.model.member
        path = '/mailings/%s/members' % self.mailing['mailing_id']
        if not self._dict:
            self._dict = dict(
                (x['member_id'], member.Member(self.mailing.account, x))
                    for x in self.mailing.account.adapter.get(path))
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

    def __delitem__(self, key):
        pass

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Search` objects

        :rtype: :class:`dict` of :class:`Search` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mlng = acct.mailings[123]
            >>> mlng.searches.fetch_all()
            {123: <Search>, 321: <Search>, ...}

        """
        if 'mailing_id' not in self.mailing:
            raise ex.NoMailingIdError()
        search = myemma.model.search
        path = '/mailings/%s/searches' % self.mailing['mailing_id']
        if not self._dict:
            self._dict = dict(
                (x['search_id'], search.Search(self.mailing.account, x))
                    for x in self.mailing.account.adapter.get(path))
        return self._dict
