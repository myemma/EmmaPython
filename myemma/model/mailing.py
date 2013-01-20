"""Audience mailing models"""

from myemma.model import BaseApiModel, str_fields_to_datetime


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

    def _parse_raw(self, raw):
        raw.update(str_fields_to_datetime(
            ['clicked', 'opened', 'delivery_ts', 'forwarded', 'shared', 'sent'],
            raw))
        return raw
