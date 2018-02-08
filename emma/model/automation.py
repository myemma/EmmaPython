"""Automation models"""

from emma.model import BaseApiModel, str_fields_to_datetime_alt


class Workflow(BaseApiModel):
    """
    Encapsulates operations for a :class:`Workflow`

    :param account: The Account which owns this Workflow
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Workflow`
    :type raw: :class:`dict`

    Usage::

        >>> from emma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> auto = acct.workflows[123]
        >>> auto
        <Workflow>
    """
    def __init__(self, account, raw=None):
        self.account = account
        super(Workflow, self).__init__(raw)

    # def __repr__(self):
    #     return '<Workflow: {}>'.format(self.workflow_id)

    def _parse_raw(self, raw):
        raw.update(
            str_fields_to_datetime_alt(
                ['created_at', 'updated_at'], raw
            )
        )
        return raw
