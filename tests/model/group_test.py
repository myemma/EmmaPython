from datetime import datetime
import unittest
from myemma import exceptions as ex
from myemma.enumerations import GroupType, MemberStatus
from myemma.model.account import Account
from myemma.model.group import Group
from myemma.model.member import Member
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

    def test_can_save_a_group(self):
        grp = Group(self.group.account, {'group_name':u"New Group"})
        MockAdapter.expected = [
            {'member_group_id': 201, 'group_name': u"New Group"}]

        result = grp.save()

        self.assertIsNone(result)
        self.assertEquals(grp.account.adapter.called, 1)
        self.assertEquals(self.group.account.adapter.call, (
            'POST',
            '/groups',
            {'groups': [{'group_name': u"New Group"}]}
        ))

    def test_can_save_a_group2(self):
        grp = Group(
            self.group.account,
            {'member_group_id': 200, 'group_name':u"Renamed Group"})
        MockAdapter.expected = False

        with self.assertRaises(ex.GroupUpdateError):
            grp.save()
        self.assertEquals(grp.account.adapter.called, 1)
        self.assertEquals(
            grp.account.adapter.call,
            ('PUT', '/groups/200', {'group_name':u"Renamed Group"}))

    def test_can_save_a_group3(self):
        grp = Group(
            self.group.account,
            {'member_group_id': 200, 'group_name':u"Renamed Group"})
        MockAdapter.expected = True

        grp.save()

        self.assertEquals(grp.account.adapter.called, 1)
        self.assertEquals(
            grp.account.adapter.call,
            ('PUT', '/groups/200', {'group_name':u"Renamed Group"}))


class GroupMemberCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.members = Group(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {'member_group_id': 200, 'group_name': u"My Group"}
        ).members

    def test_can_fetch_all_members(self):
        del(self.members.group['member_group_id'])
        with self.assertRaises(ex.NoGroupIdError):
            self.members.fetch_all()
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_fetch_all_members2(self):
        # Setup
        MockAdapter.expected = [
            {'member_id': 200, 'email': u"test01@example.org"},
            {'member_id': 201, 'email': u"test02@example.org"},
            {'member_id': 202, 'email': u"test03@example.org"}
        ]

        members = self.members.fetch_all()

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('GET', '/groups/200/members', {}))
        self.assertIsInstance(members, dict)
        self.assertEquals(3, len(members))
        self.assertEquals(3, len(self.members))
        self.assertIsInstance(self.members[200], Member)
        self.assertIsInstance(self.members[201], Member)
        self.assertIsInstance(self.members[202], Member)
        self.assertEquals(self.members[200]['email'], u"test01@example.org")
        self.assertEquals(self.members[201]['email'], u"test02@example.org")
        self.assertEquals(self.members[202]['email'], u"test03@example.org")

    def test_can_fetch_all_members3(self):
        # Setup
        MockAdapter.expected = [
            {'member_id': 204, 'email': u"test04@example.org"}
        ]

        members = self.members.fetch_all(True)

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('GET', '/groups/200/members', {'deleted': True}))
        self.assertIsInstance(members, dict)
        self.assertEquals(1, len(members))
        self.assertEquals(1, len(self.members))
        self.assertIsInstance(self.members[204], Member)
        self.assertEquals(self.members[204]['email'], u"test04@example.org")

    def test_can_add_members_by_status(self):
        del(self.members.group['member_group_id'])
        with self.assertRaises(ex.NoGroupIdError):
            self.members.add_by_status([
                MemberStatus.Active,
                MemberStatus.Error])
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_add_members_by_status2(self):
        self.members.add_by_status()
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_add_members_by_status3(self):
        MockAdapter.expected = False

        with self.assertRaises(ex.MemberCopyToGroupError):
            self.members.add_by_status([MemberStatus.Active])
        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('PUT', '/members/200/copy', {'member_status_id':[u"a"]}))

    def test_can_add_members_by_status4(self):
        MockAdapter.expected = True

        self.members.add_by_status([MemberStatus.Active])

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('PUT', '/members/200/copy', {'member_status_id':[u"a"]}))

    def test_can_add_members_by_id(self):
        del(self.members.group['member_group_id'])
        with self.assertRaises(ex.NoGroupIdError):
            self.members.add_by_id([200, 201])
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_add_members_by_id2(self):
        self.members.add_by_id()
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_add_members_by_id3(self):
        MockAdapter.expected = [200, 201]

        self.members.add_by_id([200, 201])

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('PUT', '/groups/200/members', {'member_ids':[200, 201]}))

    def test_can_add_members_by_group(self):
        del(self.members.group['member_group_id'])
        other = Group(self.members.group.account, {'member_group_id': 199})
        with self.assertRaises(ex.NoGroupIdError):
            self.members.add_by_group(other, [MemberStatus.Active])
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_add_members_by_group2(self):
        other = Group(self.members.group.account)
        with self.assertRaises(ex.NoGroupIdError):
            self.members.add_by_group(other, [MemberStatus.Active])
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_add_members_by_group3(self):
        MockAdapter.expected = True
        other = Group(self.members.group.account, {'member_group_id': 199})

        result = self.members.add_by_group(other, [MemberStatus.Active])

        self.assertIsNone(result)
        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('PUT', '/groups/199/200/members/copy', {'member_status_id': ["a"]}))

    def test_can_add_members_by_group4(self):
        MockAdapter.expected = False
        other = Group(self.members.group.account, {'member_group_id': 199})

        with self.assertRaises(ex.MemberCopyToGroupError):
            self.members.add_by_group(other, [MemberStatus.Active])

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('PUT', '/groups/199/200/members/copy', {'member_status_id': ["a"]}))

    def test_can_remove_members_by_id(self):
        del(self.members.group['member_group_id'])
        with self.assertRaises(ex.NoGroupIdError):
            self.members.remove_by_id([200, 201])
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_remove_members_by_id2(self):
        self.members.remove_by_id()
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_remove_members_by_id3(self):
        MockAdapter.expected = [200, 201]

        self.members.remove_by_id([200, 201])

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('PUT', '/groups/200/members/remove', {'member_ids':[200, 201]}))

    def test_can_remove_members_by_id4(self):
        MockAdapter.expected = [204]

        del(self.members[204])

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('PUT', '/groups/200/members/remove', {'member_ids':[204]}))

    def test_can_remove_all_members(self):
        del(self.members.group['member_group_id'])
        with self.assertRaises(ex.NoGroupIdError):
            self.members.remove_all()
        self.assertEquals(self.members.group.account.adapter.called, 0)

    def test_can_remove_all_members2(self):
        MockAdapter.expected = True
        self.members.remove_all()
        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('DELETE', '/groups/200/members', {}))

    def test_can_remove_all_members3(self):
        MockAdapter.expected = True

        self.members.remove_all(MemberStatus.Active)

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('DELETE', '/groups/200/members', {'member_status_id': u"a"}))

    def test_can_remove_all_members4(self):
        MockAdapter.expected = True

        self.members.remove_all(MemberStatus.Error)

        self.assertEquals(self.members.group.account.adapter.called, 1)
        self.assertEquals(
            self.members.group.account.adapter.call,
            ('DELETE', '/groups/200/members', {'member_status_id': u"e"}))