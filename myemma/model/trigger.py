"""Audience trigger models"""

from datetime import datetime
from myemma import exceptions as ex
from myemma.model import BaseApiModel, str_fields_to_datetime
import myemma.model.mailing


class Trigger(BaseApiModel):
    """
    Encapsulates operations for a :class:`Trigger`

    :param account: The Account which owns this Trigger
    :type account: :class:`Account`
    :param raw: The raw values of this :class:`Trigger`
    :type raw: :class:`dict`

    Usage::

        >>> from myemma.model.account import Account
        >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
        >>> acct.triggers[123]
        <Trigger>
    """
    def __init__(self, account, raw=None):
        self.account = account
        super(Trigger, self).__init__(raw)
        self.mailings = TriggerMailingCollection(self)

    def _parse_raw(self, raw):
        raw.update(str_fields_to_datetime(['deleted_at', 'start_ts'], raw))
        if 'parent_mailing' in raw:
            mailing = myemma.model.mailing
            raw['parent_mailing'] = mailing.Mailing(
                self.account,
                raw['parent_mailing'])
        return raw

    def is_deleted(self):
        """
        Whether a trigger has been deleted

        :rtype: :class:`bool`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> trggr = acct.triggers[123]
            >>> trggr.is_deleted()
            False
            >>> trggr.delete()
            >>> trggr.is_deleted()
            True
        """
        return 'deleted_at' in self._dict and bool(self._dict['deleted_at'])

    def delete(self):
        """
        Delete this trigger

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> trggr = acct.triggers[123]
            >>> trggr.delete()
            None
        """
        if not 'trigger_id' in self._dict:
            raise ex.NoTriggerIdError()
        if self.is_deleted():
            return None

        path = "/triggers/%s" % self._dict['trigger_id']
        if self.account.adapter.delete(path):
            self._dict['deleted_at'] = datetime.now()
        if self._dict['trigger_id'] in self.account.triggers:
            del(self.account.triggers._dict[self._dict['trigger_id']])

    def extract(self):
        """
        Extracts data from the model in a format suitable for using with the API

        :rtype: :class:`dict`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> trggr = acct.triggers[123]
            >>> trggr.extract()
            {'name':..., 'criteria':...}
        """
        keys = ['name', 'event_type', 'parent_mailing_id', 'groups', 'links',
                'signups', 'surveys', 'field_id', 'push_offset', 'is_disabled']

        return dict(x for x in self._dict.items() if x[0] in keys)

    def _add(self):
        """Add a single trigger"""
        path = '/triggers'
        data = self.extract()
        self._dict['trigger_id'] = self.account.adapter.post(path, data)
        self.account.triggers._dict[self._dict['trigger_id']] = self

    def _update(self):
        """Update a single trigger"""
        path = '/triggers/%s' % self._dict['trigger_id']
        data = self.extract()
        self.account.adapter.put(path, data)

    def save(self):
        """
        Add or update this :class:`Trigger`

        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> trggr = acct.triggers[123]
            >>> trggr['name'] = u"Renamed Trigger"
            >>> trggr.save()
            123
            >>> from myemma.enumerations import EventType
            >>> trggr = acct.triggers.factory(
            ...     {
            ...         'parent_mailing_id': 200,
            ...         'object_ids': [10, 20, 30],
            ...         'name': 'Test Trigger',
            ...         'event_type': EventType.Click
            ...     }
            ... )
            >>> trggr.save()
            124
        """
        if 'trigger_id' not in self._dict:
            return self._add()
        else:
            return self._update()


class TriggerMailingCollection(BaseApiModel):
    """
    Encapsulates operations for the set of :class:`Mailing` objects of a
    :class:`Trigger`

    :param trigger: The trigger which owns this collection
    :type trigger: :class:`Trigger`
    """
    def __init__(self, trigger):
        self.trigger = trigger
        super(TriggerMailingCollection, self).__init__()

    def fetch_all(self):
        """
        Lazy-loads the full set of :class:`Mailing` objects

        :rtype: :class:`dict` of :class:`Mailing` objects

        Usage::

            >>> from myemma.model.account import Account
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> trggr = acct.triggers[1024]
            >>> trggr.mailings.fetch_all()
            {200: <Mailing>, 201: <Mailing>, ...}
        """
        if not 'trigger_id' in self.trigger:
            raise ex.NoSearchIdError()

        path = '/triggers/%s/mailings' % self.trigger['trigger_id']
        if not self._dict:
            mailing = myemma.model.mailing
            self._dict = dict(
                (x['mailing_id'], mailing.Mailing(self.trigger.account, x))
                    for x in self.trigger.account.adapter.get(path))
        return self._dict
