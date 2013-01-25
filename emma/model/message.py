"""Audience mailing message models"""

from emma import exceptions as ex
from emma.model import BaseApiModel


class Message(BaseApiModel):
    """
    Encapsulates operations for a :class:`Message`

    :param mailing: The Mailing which owns this Message
    :type mailing: :class:`Mailing`
    :param member_id: The Member ID to whom this Message was sent
    :type member_id: :class:`int`
    :param raw: The raw values of this :class:`Message`
    :type raw: :class:`dict`

    Usage::

        >>> from emma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> mlng = acct.mailings[123]
        >>> mlng.messages[12]
        <Message>
    """
    def __init__(self, mailing, member_id=None, raw=None):
        self.mailing = mailing
        self.member_id = member_id
        super(Message, self).__init__(raw)

    def forward(self, emails=None, note=None):
        """
        Forward a previous message to additional recipients. If these recipients
        are not already in the audience, they will be added with a status of
        FORWARDED.

        :param emails: The emails to receive this forward
        :type emails: :class:`list` of :class:`str`
        :param note: A note to be sent with this forward
        :type note: :class:`str`
        :rtype: :class:`int`

        Usage::

            >>> from emma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> mssg = acct.mailings[123].messages[12]
            >>> mssg.forward(["test2@example.com", "test3@example.com"])
            124
        """
        if 'mailing_id' not in self.mailing:
            raise ex.NoMailingIdError()
        if not self.member_id:
            raise ex.NoMemberIdError()
        if not emails:
            return None

        path = "/forwards/%s/%s" % (self.mailing['mailing_id'], self.member_id)
        data = {'recipient_emails': emails}
        if note:
            data['note'] = note

        result = self.mailing.account.adapter.post(path, data)

        if not result:
            raise ex.MailingForwardError()

        return result['mailing_id']
