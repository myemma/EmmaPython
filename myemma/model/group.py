from . import BaseApiModel, ModelWithDateFields, MemberCopyToGroupError
import group_type


class NoGroupIdError(Exception): pass


class Group(BaseApiModel, ModelWithDateFields):
    def __init__(self, account, raw=None):
        self.account = account
        super(Group, self).__init__(raw)

    def _parse_raw(self, raw):
        if 'group_type' in raw:
            raw['group_type'] = group_type.GroupType.factory(raw['group_type'])
        self._str_fields_to_datetime(['deleted_at'], raw)
        return raw

    def collect_members_by_status(self, statuses=None):
        """
        Makes all members of a particular status part of this group

        :param statuses: Set of statuses to collect
        :type statuses: :class:`list` of :class:`MemberStatus`
        :rtype: :class:`None`

        Usage::

            >>> from myemma.model.account import Account
            >>> from myemma.model.member_status import Active
            >>> acct = Account(1234, "08192a3b4c5d6e7f", "f7e6d5c4b3a29180")
            >>> grp = acct.groups[1024]
            >>> grp.collect_members_by_status([Active])
            None
        """
        if 'member_group_id' not in self._dict:
            raise NoGroupIdError()
        if not statuses:
            return None

        path = '/members/%s/copy' % self._dict['member_group_id']
        data = {'member_status_id': map(lambda x: x.get_code(), statuses)}
        if not self.account.adapter.put(path, data):
            raise MemberCopyToGroupError()
