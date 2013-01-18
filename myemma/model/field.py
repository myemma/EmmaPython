from datetime import datetime
from myemma.adapter import NoFieldIdError
from . import BaseApiModel


class Field(BaseApiModel):
    def __init__(self, account, raw=None):
        self.account = account
        super(Field, self).__init__(raw)

    def is_deleted(self):
        """
        Whether a field has been deleted

        :rtype: :class:`bool`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> fld = acct.fields[123]
            >>> fld.is_deleted()
            False
            >>> fld.delete()
            >>> fld.is_deleted()
            True
        """
        return 'deleted_at' in self._dict and self._dict['deleted_at']

    def delete(self):
        """
        Delete this field

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> fld = acct.fields[123]
            >>> fld.delete()
            None
        """
        if not 'field_id' in self._dict:
            raise NoFieldIdError()
        if self.is_deleted():
            return None

        path = "/fields/%s" % self._dict['field_id']
        if self.account.adapter.delete(path):
            self._dict['deleted_at'] = datetime.now()
