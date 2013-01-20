from datetime import datetime
import unittest
from myemma import exceptions as ex
from myemma.enumerations import GroupType, MemberStatus
from myemma.model.account import Account
from myemma.model.group import Group
from myemma.model import SERIALIZED_DATETIME_FORMAT
from tests.model import MockAdapter


class GroupTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.group = Group(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'group_name': u"Test Group",
                'group_type': GroupType.RegularGroup,
                'deleted_at': None
            }
        )

    def test_can_parse_special_fields_correctly(self):
        self.assertEquals(self.group['group_type'], GroupType.RegularGroup)
        self.assertIsNone(self.group['deleted_at'])

    def test_can_collect_members_by_status(self):
        with self.assertRaises(ex.NoGroupIdError):
            self.group.collect_members_by_status([
                MemberStatus.Active,
                MemberStatus.Error])
        self.assertEquals(self.group.account.adapter.called, 0)

    def test_can_collect_members_by_status2(self):
        self.group['member_group_id'] = 200
        self.group.collect_members_by_status()
        self.assertEquals(self.group.account.adapter.called, 0)

    def test_can_collect_members_by_status3(self):
        self.group['member_group_id'] = 200
        MockAdapter.expected = False

        with self.assertRaises(ex.MemberCopyToGroupError):
            self.group.collect_members_by_status([MemberStatus.Active])
        self.assertEquals(self.group.account.adapter.called, 1)
        self.assertEquals(
            self.group.account.adapter.call,
            ('PUT', '/members/200/copy', {'member_status_id':[u"a"]}))

    def test_can_collect_members_by_status4(self):
        self.group['member_group_id'] = 200
        MockAdapter.expected = True

        self.group.collect_members_by_status([MemberStatus.Active])

        self.assertEquals(self.group.account.adapter.called, 1)
        self.assertEquals(
            self.group.account.adapter.call,
            ('PUT', '/members/200/copy', {'member_status_id':[u"a"]}))

    def test_can_delete_a_group(self):
        grp = Group(self.group.account)

        with self.assertRaises(ex.NoGroupIdError):
            grp.delete()
        self.assertEquals(self.group.account.adapter.called, 0)
        self.assertFalse(self.group.is_deleted())

    def test_can_delete_a_group2(self):
        MockAdapter.expected = None
        grp = Group(
            self.group.account,
            {
                'member_group_id': 200,
                'deleted_at': datetime.now().strftime(SERIALIZED_DATETIME_FORMAT)
            })

        result = grp.delete()

        self.assertIsNone(result)
        self.assertEquals(grp.account.adapter.called, 0)
        self.assertTrue(grp.is_deleted())

    def test_can_delete_a_group3(self):
        MockAdapter.expected = True
        mbr = Group(
            self.group.account,
            {
                'member_group_id': 200,
                'deleted_at': None
            })

        result = mbr.delete()

        self.assertIsNone(result)
        self.assertEquals(mbr.account.adapter.called, 1)
        self.assertEquals(
            mbr.account.adapter.call,
            ('DELETE', '/groups/200', {}))
        self.assertTrue(mbr.is_deleted())
