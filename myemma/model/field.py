"""Audience field models"""

from datetime import datetime
from myemma import exceptions as ex
from myemma.model import BaseApiModel, str_fields_to_datetime


class Field(BaseApiModel):
    """
    Encapsulates operations for a :class:`Field`

    :param account: The Account which owns this Field
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Field`
    :type raw: :class:`dict`

    Usage::

        >>> from myemma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> fld = acct.fields[123]
        >>> fld
        <Field>
    """
    def __init__(self, account, raw=None):
        self.account = account
        super(Field, self).__init__(raw)

    def _parse_raw(self, raw):
        raw.update(str_fields_to_datetime(['deleted_at'], raw))
        return raw

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
        return 'deleted_at' in self._dict and bool(self._dict['deleted_at'])

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
            raise ex.NoFieldIdError()
        if self.is_deleted():
            return None

        path = "/fields/%s" % self._dict['field_id']
        if self.account.adapter.delete(path):
            self._dict['deleted_at'] = datetime.now()
        if self._dict['field_id'] in self.account.fields:
            del(self.account.fields._dict[self._dict['field_id']])

    def extract(self):
        """
        Extracts data from the model in a format suitable for using with the API

        :rtype: :class:`dict`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> fld = acct.fields[123]
            >>> fld.extract()
            {'field_id':123, 'shortcut_name':u"test_field", ...}
        """
        keys = ['display_name', 'field_type', 'widget_type', 'column_order',
                'shortcut_name', 'options']

        return dict(x for x in self._dict.items() if x[0] in keys)

    def _add(self):
        """Add a single field"""
        path = '/fields'
        data = self.extract()
        self._dict['field_id'] = self.account.adapter.post(path, data)
        self.account.fields._dict[self._dict['field_id']] = self

    def _update(self):
        """Update a single field"""
        path = '/fields/%s' % self._dict['field_id']
        data = self.extract()
        self.account.adapter.put(path, data)

    def save(self):
        """
        Add or update this :class:`Field`

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> fld = acct.members[123]
            >>> fld['shortcut_name'] = u"new_name"
            >>> fld.save()
            None
            >>> fld = acct.members.factory({'shortcut_name': u"test_field"})
            >>> fld.save()
            None
        """
        if 'field_id' not in self._dict:
            return self._add()
        else:
            return self._update()

    def clear_member_information(self):
        """
        Clear all member information for this field

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> fld = acct.members[123]
            >>> fld.clear_member_information()
            None
        """
        if 'field_id' not in self._dict:
            raise ex.NoFieldIdError()

        path = '/fields/%s/clear' % self._dict['field_id']

        if not self.account.adapter.post(path):
            raise ex.ClearMemberFieldInformationError()
