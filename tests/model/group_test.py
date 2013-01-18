import unittest
from myemma.adapter import AbstractAdapter
from myemma.model import MemberCopyToGroupError
from myemma.model.account import Account
from myemma.model.group import (Group, NoGroupIdError)
from myemma.model import group_type, member_status


class MockAdapter(AbstractAdapter):
    expected = None

    def __init__(self, *args, **kwargs):
        self.called = 0
        self.call = ()

    def _capture(self, method, path, params):
        self.called += 1
        self.call = (method, path, params)

    def get(self, path, params=None):
        self._capture('GET', path, params if params else {})
        return self.__class__.expected

    def post(self, path, data=None):
        self._capture('POST', path, data if data else {})
        return self.__class__.expected

    def put(self, path, data=None):
        self._capture('PUT', path, data if data else {})
        return self.__class__.expected

    def delete(self, path, params=None):
        self._capture('DELETE', path, params if params else {})
        return self.__class__.expected


class GroupTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.group = Group(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'group_name': u"Test Group",
                'group_type': group_type.RegularGroup.get_code()
            }
        )

    def test_can_parse_special_fields_correctly(self):
        self.assertEquals(self.group['group_type'], group_type.RegularGroup)

    def test_can_collect_members_by_status(self):
        with self.assertRaises(NoGroupIdError):
            self.group.collect_members_by_status([
                member_status.Active,
                member_status.Error])
        self.assertEquals(self.group.account.adapter.called, 0)

    def test_can_collect_members_by_status2(self):
        self.group['member_group_id'] = 200
        self.group.collect_members_by_status()
        self.assertEquals(self.group.account.adapter.called, 0)

    def test_can_collect_members_by_status3(self):
        self.group['member_group_id'] = 200
        MockAdapter.expected = False

        with self.assertRaises(MemberCopyToGroupError):
            self.group.collect_members_by_status([member_status.Active])
        self.assertEquals(self.group.account.adapter.called, 1)
        self.assertEquals(
            self.group.account.adapter.call,
            ('PUT', '/members/200/copy', {'member_status_id':[u"a"]}))

    def test_can_collect_members_by_status4(self):
        self.group['member_group_id'] = 200
        MockAdapter.expected = True

        self.group.collect_members_by_status([member_status.Active])

        self.assertEquals(self.group.account.adapter.called, 1)
        self.assertEquals(
            self.group.account.adapter.call,
            ('PUT', '/members/200/copy', {'member_status_id':[u"a"]}))
