import unittest
from myemma.adapter import AbstractAdapter
from myemma.adapter.requests_adapter import RequestsAdapter
from myemma.model import (NoMemberEmailError, MemberDeleteError,
                          MemberChangeStatusError, MemberDropGroupError,
                          ImportDeleteError)
from myemma.model.account import (Account, AccountFieldCollection,
                                  AccountImportCollection,
                                  AccountMemberCollection,
                                  AccountGroupCollection)
from myemma.model.field import Field
from myemma.model.group import Group
from myemma.model.member_import import MemberImport
from myemma.model.member import Member
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


class AccountDefaultAdapterTest(unittest.TestCase):
    def test_default_adapter_is_api_v1_adapter(self):
        self.assertIs(Account.default_adapter, RequestsAdapter)


class AccountTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.account = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy")

    def test_field_collection_can_be_accessed(self):
        self.assertIsInstance(self.account.fields, AccountFieldCollection)

    def test_import_collection_can_be_accessed(self):
        self.assertIsInstance(self.account.imports, AccountImportCollection)

    def test_member_collection_can_be_accessed(self):
        self.assertIsInstance(self.account.members, AccountMemberCollection)


class AccountFieldCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.fields = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy").fields

    def test_fetch_all_returns_a_dictionary(self):
        MockAdapter.expected = [{'field_id': 201}]
        self.assertIsInstance(self.fields.fetch_all(), dict)
        self.assertEquals(self.fields.account.adapter.called, 1)
        self.assertEquals(
            self.fields.account.adapter.call,
            ('GET', '/fields', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{'field_id': 201}]
        self.assertEquals(0, len(self.fields))
        self.fields.fetch_all()
        self.assertEquals(1, len(self.fields))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{'field_id': 201}]
        self.fields.fetch_all()
        self.fields.fetch_all()
        self.assertEquals(self.fields.account.adapter.called, 1)

    def test_field_collection_object_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{'field_id': 201}]
        self.fields.fetch_all()
        self.assertIsInstance(self.fields, AccountFieldCollection)
        self.assertEquals(1, len(self.fields))
        self.assertIsInstance(self.fields[201], Field)

    def test_field_collection_can_export_list_of_valid_shortcut_names(self):
        MockAdapter.expected = [
            {'field_id': 200, 'shortcut_name': u"first_name"},
            {'field_id': 201, 'shortcut_name': u"last_name"},
            {'field_id': 202, 'shortcut_name': u"work_phone"}]
        shortcuts = self.fields.export_shortcuts()
        self.assertIsInstance(shortcuts, list)
        self.assertEquals(3, len(shortcuts))
        self.assertListEqual(
            shortcuts,
            [u"first_name", u"last_name", u"work_phone"]
        )


class AccountGroupCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.groups = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy").groups

    def test_fetch_all_returns_a_dictionary(self):
        MockAdapter.expected = [{'member_group_id': 201}]
        self.assertIsInstance(self.groups.fetch_all(), dict)
        self.assertEquals(self.groups.account.adapter.called, 1)
        self.assertEquals(
            self.groups.account.adapter.call,
            ('GET', '/groups', {}))

    def test_fetch_all_returns_a_dictionary2(self):
        MockAdapter.expected = [{'member_group_id': 201}]
        self.assertIsInstance(
            self.groups.fetch_all([
                group_type.RegularGroup,
                group_type.HiddenGroup]),
            dict)
        self.assertEquals(self.groups.account.adapter.called, 1)
        self.assertEquals(
            self.groups.account.adapter.call,
            ('GET', '/groups', {'group_types': [u"g", u"h"]}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{'member_group_id': 201}]
        self.assertEquals(0, len(self.groups))
        self.groups.fetch_all()
        self.assertEquals(1, len(self.groups))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{'member_group_id': 201}]
        self.groups.fetch_all()
        self.groups.fetch_all()
        self.assertEquals(self.groups.account.adapter.called, 1)

    def test_group_collection_object_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{'member_group_id': 201}]
        self.groups.fetch_all()
        self.assertIsInstance(self.groups, AccountGroupCollection)
        self.assertEquals(1, len(self.groups))
        self.assertIsInstance(self.groups[201], Group)

    def test_fetch_one_by_group_id_populates_collection(self):
        MockAdapter.expected = {'member_group_id': 201}
        self.groups.find_one_by_group_id(201)
        self.assertIn(201, self.groups)
        self.assertIsInstance(self.groups[201], Group)
        self.assertEquals(self.groups[201]['member_group_id'], 201)

    def test_fetch_one_by_import_id_caches_result(self):
        MockAdapter.expected = {'member_group_id': 201}
        self.groups.find_one_by_group_id(201)
        self.groups.find_one_by_group_id(201)
        self.assertEquals(self.groups.account.adapter.called, 1)

    def test_dictionary_access_lazy_loads_by_import_id(self):
        MockAdapter.expected = {'member_group_id': 201}
        group = self.groups[201]
        self.assertIn(201, self.groups)
        self.assertIsInstance(group, Group)
        self.assertEquals(self.groups[201]['member_group_id'], 201)
        self.assertEquals(self.groups.account.adapter.called, 1)
        self.assertEquals(
            self.groups.account.adapter.call,
            ('GET', '/groups/201', {}))

    def test_dictionary_access_lazy_loads_by_import_id2(self):
        MockAdapter.expected = None
        group = self.groups[204]
        self.assertEquals(0, len(self.groups))
        self.assertIsNone(group)
        self.assertEquals(self.groups.account.adapter.called, 1)
        self.assertEquals(
            self.groups.account.adapter.call,
            ('GET', '/groups/204', {}))


class AccountImportCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.imports = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy").imports

    def test_fetch_all_returns_a_dictionary(self):
        MockAdapter.expected = [{'import_id': 201}]
        self.assertIsInstance(self.imports.fetch_all(), dict)
        self.assertEquals(self.imports.account.adapter.called, 1)
        self.assertEquals(
            self.imports.account.adapter.call,
            ('GET', '/members/imports', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{'import_id': 201}]
        self.assertEquals(0, len(self.imports))
        self.imports.fetch_all()
        self.assertEquals(1, len(self.imports))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{'import_id': 201}]
        self.imports.fetch_all()
        self.imports.fetch_all()
        self.assertEquals(self.imports.account.adapter.called, 1)

    def test_imports_collection_object_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{'import_id': 201}]
        self.imports.fetch_all()
        self.assertIsInstance(self.imports, AccountImportCollection)
        self.assertEquals(1, len(self.imports))
        self.assertIsInstance(self.imports[201], MemberImport)

    def test_fetch_one_by_import_id_returns_an_import_object(self):
        MockAdapter.expected = {'import_id': 201}
        emma_import = self.imports.find_one_by_import_id(201)
        self.assertIsInstance(emma_import, MemberImport)
        self.assertEquals(emma_import['import_id'], 201)
        self.assertEquals(self.imports.account.adapter.called, 1)
        self.assertEquals(
            self.imports.account.adapter.call,
            ('GET', '/members/imports/201', {}))

    def test_fetch_one_by_import_id_populates_collection(self):
        MockAdapter.expected = {'import_id': 201}
        self.imports.find_one_by_import_id(201)
        self.assertIn(201, self.imports)
        self.assertIsInstance(self.imports[201], MemberImport)
        self.assertEquals(self.imports[201]['import_id'], 201)

    def test_fetch_one_by_import_id_caches_result(self):
        MockAdapter.expected = {'import_id': 201}
        self.imports.find_one_by_import_id(201)
        self.imports.find_one_by_import_id(201)
        self.assertEquals(self.imports.account.adapter.called, 1)

    def test_dictionary_access_lazy_loads_by_import_id(self):
        MockAdapter.expected = {'import_id': 201}
        emma_import = self.imports[201]
        self.assertIn(201, self.imports)
        self.assertIsInstance(emma_import, MemberImport)
        self.assertEquals(self.imports[201]['import_id'], 201)
        self.assertEquals(self.imports.account.adapter.called, 1)
        self.assertEquals(
            self.imports.account.adapter.call,
            ('GET', '/members/imports/201', {}))

    def test_dictionary_access_lazy_loads_by_import_id2(self):
        MockAdapter.expected = None
        emma_import = self.imports[204]
        self.assertEquals(0, len(self.imports))
        self.assertIsNone(emma_import)
        self.assertEquals(self.imports.account.adapter.called, 1)
        self.assertEquals(
            self.imports.account.adapter.call,
            ('GET', '/members/imports/204', {}))

    def test_can_mark_imports_as_deleted(self):
        # Setup
        MockAdapter.expected = True
        self.imports._dict = {
            203: MemberImport(self.imports.account),
            204: MemberImport(self.imports.account),
            205: MemberImport(self.imports.account)
        }

        result = self.imports.delete([204, 205])
        self.assertIsNone(result)
        self.assertEquals(self.imports.account.adapter.called, 1)
        self.assertEquals(
            self.imports.account.adapter.call,
            ('DELETE', '/members/imports/delete', {'import_ids': [204, 205]}))
        self.assertEquals(1, len(self.imports))
        self.assertIn(203, self.imports)

    def test_can_mark_imports_as_deleted(self):
        result = self.imports.delete()
        self.assertIsNone(result)
        self.assertEquals(self.imports.account.adapter.called, 0)

    def test_can_mark_imports_as_deleted2(self):
        # Setup
        MockAdapter.expected = False
        self.imports._dict = {
            203: MemberImport(self.imports.account),
            204: MemberImport(self.imports.account),
            205: MemberImport(self.imports.account)
        }

        with self.assertRaises(ImportDeleteError):
            self.imports.delete([204, 205])

        self.assertEquals(self.imports.account.adapter.called, 1)
        self.assertEquals(
            self.imports.account.adapter.call,
            ('DELETE', '/members/imports/delete', {'import_ids': [204, 205]}))
        self.assertEquals(3, len(self.imports))

    def test_can_mark_imports_as_deleted3(self):
        # Setup
        MockAdapter.expected = True
        self.imports._dict = {
            203: MemberImport(self.imports.account),
            204: MemberImport(self.imports.account),
            205: MemberImport(self.imports.account)
        }

        result = self.imports.delete([204, 205])
        self.assertIsNone(result)
        self.assertEquals(self.imports.account.adapter.called, 1)
        self.assertEquals(
            self.imports.account.adapter.call,
            ('DELETE', '/members/imports/delete', {'import_ids': [204, 205]}))
        self.assertEquals(1, len(self.imports))
        self.assertIn(203, self.imports)


class AccountMemberCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.members = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy").members

    def test_fetch_all_returns_a_dictionary(self):
        # Setup
        MockAdapter.expected = [{'member_id': 201}]

        self.assertIsInstance(self.members.fetch_all(), dict)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members', {}))

    def test_fetch_all_returns_a_dictionary2(self):
        # Setup
        MockAdapter.expected = [{'member_id': 201},{'member_id': 204}]

        self.assertIsInstance(self.members.fetch_all(deleted=True), dict)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members', {"deleted":True}))

    def test_fetch_all_populates_collection(self):
        # Setup
        MockAdapter.expected = [{'member_id': 201}]
        self.assertEquals(0, len(self.members))

        self.members.fetch_all()

        self.assertEquals(1, len(self.members))

    def test_fetch_all_caches_results(self):
        # Setup
        MockAdapter.expected = [{'member_id': 201}]

        self.members.fetch_all()
        self.members.fetch_all()

        self.assertEquals(self.members.account.adapter.called, 1)

    def test_members_collection_object_can_be_accessed_like_a_dictionary(self):
        # Setup
        MockAdapter.expected = [{'member_id': 201}]

        self.members.fetch_all()

        self.assertIsInstance(self.members, AccountMemberCollection)
        self.assertEquals(1, len(self.members))
        self.assertIsInstance(self.members[201], Member)

    def test_fetch_all_by_import_id_returns_a_dictionary(self):
        # Setup
        MockAdapter.expected = [{'member_id': 201}]

        self.assertIsInstance(self.members.fetch_all_by_import_id(100), dict)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/imports/100/members', {}))

    def test_fetch_all_by_import_id_updates_collection(self):
        # Setup
        MockAdapter.expected = [{'member_id': 201}]
        self.assertEquals(0, len(self.members))

        self.members.fetch_all_by_import_id(100)

        self.assertEquals(1, len(self.members))

    def test_fetch_all_by_import_id_updates_collection2(self):
        # Setup
        self.members._dict = {
            200: {'member_id': 200, 'email': u"test1@example.com"},
            201: {'member_id': 201, 'email': u"test2@example.com"}
        }
        MockAdapter.expected = [
            {'member_id': 201, 'email': u"test3@example.com"}
        ]
        self.assertEquals(2, len(self.members))

        self.members.fetch_all_by_import_id(100)

        self.assertEquals(2, len(self.members))
        self.assertDictEqual(
            self.members._dict,
            {
                200: {'member_id': 200, 'email': u"test1@example.com"},
                201: {'member_id': 201, 'email': u"test3@example.com"}
            }
        )

    def test_fetch_all_by_import_id_updates_collection3(self):
        # Setup
        self.members._dict = {
            200: {'member_id': 200, 'email': u"test1@example.com"},
            201: {'member_id': 201, 'email': u"test2@example.com"}
        }
        MockAdapter.expected = [
            {'member_id': 201, 'email': u"test3@example.com"},
            {'member_id': 202, 'email': u"test4@example.com"}
        ]
        self.assertEquals(2, len(self.members))

        self.members.fetch_all_by_import_id(100)

        self.assertEquals(3, len(self.members))
        self.assertDictEqual(
            self.members._dict,
            {
                200: {'member_id': 200, 'email': u"test1@example.com"},
                201: {'member_id': 201, 'email': u"test3@example.com"},
                202: {'member_id': 202, 'email': u"test4@example.com"}
            }
        )

    def test_fetch_all_by_import_id_updates_collection4(self):
        # Setup
        self.members._dict = {
            201: {'member_id': 201, 'email': u"test2@example.com"}
        }
        MockAdapter.expected = [
            {'member_id': 201, 'email': u"test3@example.com"}
        ]
        self.assertEquals(1, len(self.members))

        self.members.fetch_all_by_import_id(100)

        self.assertEquals(1, len(self.members))
        self.assertDictEqual(
            self.members._dict,
            {
                201: {'member_id': 201, 'email': u"test3@example.com"}
            }
        )

    def test_fetch_all_by_import_id_does_not_cache_results(self):
        # Setup
        MockAdapter.expected = [{'member_id': 201}]

        self.members.fetch_all_by_import_id(100)
        self.members.fetch_all_by_import_id(100)

        self.assertEquals(self.members.account.adapter.called, 2)

    def test_fetch_one_by_member_id_returns_a_member_object(self):
        # Setup
        MockAdapter.expected = {'member_id': 201}

        member = self.members.find_one_by_member_id(201)

        self.assertIsInstance(member, Member)
        self.assertEquals(member['member_id'], 201)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/201', {}))

    def test_fetch_one_by_member_id_returns_a_member_object2(self):
        # Setup
        MockAdapter.expected = {'member_id': 204}

        member = self.members.find_one_by_member_id(204, deleted=True)

        self.assertIsInstance(member, Member)
        self.assertEquals(member['member_id'], 204)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/204', {"deleted":True}))

    def test_fetch_one_by_member_id_populates_collection(self):
        # Setup
        MockAdapter.expected = {'member_id': 201}

        self.members.find_one_by_member_id(201)

        self.assertIn(201, self.members)
        self.assertIsInstance(self.members[201], Member)
        self.assertEquals(self.members[201]['member_id'], 201)

    def test_fetch_one_by_member_id_caches_result(self):
        # Setup
        MockAdapter.expected = {'member_id': 201}

        self.members.find_one_by_member_id(201)
        self.members.find_one_by_member_id(201)

        self.assertEquals(self.members.account.adapter.called, 1)

    def test_dictionary_access_lazy_loads_by_member_id(self):
        # Setup
        MockAdapter.expected = {'member_id': 201}

        member = self.members[201]

        self.assertIn(201, self.members)
        self.assertIsInstance(member, Member)
        self.assertEquals(self.members[201]['member_id'], 201)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/201', {}))

    def test_dictionary_access_lazy_loads_by_member_id2(self):
        # Setup
        MockAdapter.expected = None

        member = self.members[204]

        self.assertEquals(0, len(self.members))
        self.assertIsNone(member)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/204', {}))

    def test_fetch_one_by_email_returns_a_member_object(self):
        # Setup
        MockAdapter.expected = {'member_id': 201, 'email': u"test@example.com"}

        member = self.members.find_one_by_email("test@example.com")

        self.assertIsInstance(member, Member)
        self.assertEquals(member['member_id'], 201)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_fetch_one_by_email_returns_a_member_object2(self):
        # Setup
        MockAdapter.expected = {'member_id': 204, 'email': u"test@example.com"}

        member = self.members.find_one_by_email("test@example.com", deleted=True)

        self.assertIsInstance(member, Member)
        self.assertEquals(member['member_id'], 204)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/email/test@example.com', {"deleted":True}))

    def test_fetch_one_by_email_populates_collection(self):
        # Setup
        MockAdapter.expected = {'member_id': 201, 'email': u"test@example.com"}

        self.members.find_one_by_email("test@example.com")

        self.assertIn(201, self.members)
        self.assertIsInstance(self.members[201], Member)
        self.assertEquals(self.members[201]['member_id'], 201)

    def test_fetch_one_by_email_caches_result(self):
        # Setup
        MockAdapter.expected = {'member_id': 201, 'email': u"test@example.com"}

        self.members.find_one_by_email("test@example.com")
        self.members.find_one_by_email("test@example.com")

        self.assertEquals(self.members.account.adapter.called, 1)

    def test_dictionary_access_lazy_loads_by_email(self):
        # Setup
        MockAdapter.expected = {'member_id': 201, 'email': u"test@example.com"}

        member = self.members["test@example.com"]

        self.assertIn(201, self.members)
        self.assertIsInstance(member, Member)
        self.assertEquals(self.members[201]['member_id'], 201)
        self.assertEquals(self.members[201]['email'], u"test@example.com")
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_dictionary_access_lazy_loads_by_email2(self):
        # Setup
        MockAdapter.expected = {'member_id': 201, 'email': u"test@example.com"}

        member = self.members[u"test@example.com"]

        self.assertIn(201, self.members)
        self.assertIsInstance(member, Member)
        self.assertEquals(self.members[201]['member_id'], 201)
        self.assertEquals(self.members[201]['email'], u"test@example.com")
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_dictionary_access_lazy_loads_by_email3(self):
        # Setup
        MockAdapter.expected = None

        member = self.members["test@example.com"]

        self.assertEquals(0, len(self.members))
        self.assertIsNone(member)
        self.assertEquals(1, self.members.account.adapter.called)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_dictionary_access_lazy_loads_by_email4(self):
        # Setup
        MockAdapter.expected = None

        member = self.members[u"test@example.com"]

        self.assertEquals(0, len(self.members))
        self.assertIsNone(member)
        self.assertEquals(1, self.members.account.adapter.called)
        self.assertEquals(
            self.members.account.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_can_add_members_in_bulk(self):
        MockAdapter.expected = {'import_id': 1024}
        import_id = self.members.save()
        self.assertIsNone(import_id)
        self.assertEquals(self.members.account.adapter.called, 0)

    def test_can_add_members_in_bulk2(self):
        # Setup
        MockAdapter.expected = {'import_id': 1024}
        self.members.account.fields._dict = {
            2000: {'shortcut_name': u"first_name"},
            2001: {'shortcut_name': u"last_name"}
        }

        # Attempt save
        with self.assertRaises(NoMemberEmailError):
            self.members.save([
                Member(self.members.account),
                Member(self.members.account)
            ])

        self.assertEquals(self.members.account.adapter.called, 0)

    def test_can_add_members_in_bulk3(self):
        # Setup
        MockAdapter.expected = {'import_id': 1024}
        self.members.account.fields._dict = {
            2000: {'shortcut_name': u"first_name"},
            2001: {'shortcut_name': u"last_name"}
        }

        # Perform add
        import_id = self.members.save([
            self.members.factory({
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            }),
            self.members.factory({
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        ])

        self.assertIsInstance(import_id, dict)
        self.assertTrue(import_id.has_key('import_id'))
        self.assertEquals(import_id['import_id'], 1024)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'POST',
            '/members',
            {
                'members': [
                    {'email': u"test1@example.com"},
                    {
                        'email': u"test2@example.com",
                        'fields': {'first_name': u"Emma"}
                    }
                ]
            }
        ))

    def test_can_add_members_in_bulk4(self):
        # Setup
        MockAdapter.expected = {'import_id': 1024}
        self.members.account.fields._dict = {
            2000: {'shortcut_name': u"first_name"},
            2001: {'shortcut_name': u"last_name"}
        }
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        }

        # Perform update
        import_id = self.members.save()

        self.assertIsInstance(import_id, dict)
        self.assertTrue(import_id.has_key('import_id'))
        self.assertEquals(import_id['import_id'], 1024)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'POST',
            '/members',
            {
                'members': [
                    {
                        'member_id': 200,
                        'email': u"test1@example.com"},
                    {
                        'member_id': 201,
                        'email': u"test2@example.com",
                        'fields': {'first_name': u"Emma"}}
                ]
            }
        ))

    def test_can_add_members_in_bulk5(self):
        # Setup
        MockAdapter.expected = {'import_id': 1024}
        self.members.account.fields._dict = {
            2000: {'shortcut_name': u"first_name"},
            2001: {'shortcut_name': u"last_name"}
        }
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            })
        }

        # Perform add & update
        import_id = self.members.save([
            self.members.factory({
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        ])

        self.assertIsInstance(import_id, dict)
        self.assertTrue(import_id.has_key('import_id'))
        self.assertEquals(import_id['import_id'], 1024)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'POST',
            '/members',
            {
                'members': [
                    {
                        'email': u"test2@example.com",
                        'fields': {'first_name': u"Emma"}},
                    {
                        'member_id': 200,
                        'email': u"test1@example.com"}

                ]
            }
        ))

    def test_can_add_members_in_bulk6(self):
        # Setup
        MockAdapter.expected = {'import_id': 1024}
        self.members.account.fields._dict = {
            2000: {'shortcut_name': u"first_name"},
            2001: {'shortcut_name': u"last_name"}
        }

        # Perform save with "add-only"
        import_id = self.members.save([
            self.members.factory({
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            }),
            self.members.factory({
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        ], add_only=True)

        self.assertIsInstance(import_id, dict)
        self.assertTrue(import_id.has_key('import_id'))
        self.assertEquals(import_id['import_id'], 1024)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'POST',
            '/members',
            {
                'members': [
                    {'email': u"test1@example.com"},
                    {'email': u"test2@example.com",
                     'fields': {'first_name': u"Emma"}}
                ],
                'add_only': True
            }
        ))

    def test_can_add_members_in_bulk7(self):
        # Setup
        MockAdapter.expected = {'import_id': 1024}
        self.members.account.fields._dict = {
            2000: {'shortcut_name': u"first_name"},
            2001: {'shortcut_name': u"last_name"}
        }
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        }

        # Perform save with "add-only"
        import_id = self.members.save(add_only=True)

        self.assertIsNone(import_id, None)
        self.assertEquals(self.members.account.adapter.called, 0)

    def test_can_add_members_in_bulk8(self):
        # Setup
        MockAdapter.expected = {'import_id': 1024}
        self.members.account.fields._dict = {
            2000: {'shortcut_name': u"first_name"},
            2001: {'shortcut_name': u"last_name"}
        }
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            })
        }

        # Perform save with "add-only"
        import_id = self.members.save([
            self.members.factory({
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        ], add_only=True)

        self.assertIsInstance(import_id, dict)
        self.assertTrue(import_id.has_key('import_id'))
        self.assertEquals(import_id['import_id'], 1024)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'POST',
            '/members',
            {
                'members': [
                    {
                        'email': u"test2@example.com",
                        'fields': {'first_name': u"Emma"}}

                ],
                'add_only': True
            }
        ))

    def test_can_add_members_in_bulk9(self):
        # Setup
        MockAdapter.expected = {'import_id': 1024}
        self.members.account.fields._dict = {
            2000: {'shortcut_name': u"first_name"},
            2001: {'shortcut_name': u"last_name"}
        }

        # Perform add
        import_id = self.members.save([
            self.members.factory({
                'email': u"test1@example.com"
            })
        ], filename="test.csv", group_ids=[300, 301, 302])

        self.assertIsInstance(import_id, dict)
        self.assertTrue(import_id.has_key('import_id'))
        self.assertEquals(import_id['import_id'], 1024)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'POST',
            '/members',
            {
                'members': [{'email': u"test1@example.com"}],
                'filename': u"test.csv",
                'group_ids': [300, 301, 302]
            }
        ))

    def test_can_delete_members_in_bulk(self):
        # Setup
        MockAdapter.expected = False
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        }

        with self.assertRaises(MemberDeleteError):
            self.members.delete([200, 201])

        self.assertEquals(2, len(self.members))
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'PUT',
            '/members/delete',
            {'member_ids': [200, 201]}
        ))

    def test_can_delete_members_in_bulk2(self):
        # Setup
        MockAdapter.expected = True
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        }

        self.members.delete([200])

        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'PUT',
            '/members/delete',
            {'member_ids': [200]}
        ))
        self.assertEquals(1, len(self.members))
        self.assertNotIn(200, self.members)
        self.assertIsInstance(self.members[201], Member)

    def test_can_delete_members_in_bulk3(self):
        # Setup
        MockAdapter.expected = True
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'does_not_exist': u"A member field which does not exist"
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'first_name': u"Emma"
            })
        }

        self.members.delete([200, 201])

        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'PUT',
            '/members/delete',
            {'member_ids': [200, 201]}
            ))
        self.assertEquals(0, len(self.members))

    def test_can_delete_members_by_status(self):
        # Setup
        MockAdapter.expected = False
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'status': member_status.Active.get_name()
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'status': member_status.OptOut.get_name()
            })
        }

        with self.assertRaises(MemberDeleteError):
            self.members.delete_by_status(member_status.OptOut)

        self.assertEquals(2, len(self.members))
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('DELETE', '/members', {'member_status_id': u"o"})
        )

    def test_can_delete_members_by_status2(self):
        # Setup
        MockAdapter.expected = True
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'status': member_status.Active.get_name()
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'status': member_status.OptOut.get_name()
            })
        }

        result = self.members.delete_by_status(member_status.OptOut)

        self.assertIsNone(result)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(
            self.members.account.adapter.call,
            ('DELETE', '/members', {'member_status_id': u"o"})
        )
        self.assertEquals(1, len(self.members))
        self.assertIsInstance(self.members[200], Member)

    def test_can_change_status_of_members_in_bulk(self):
        self.members.change_status_by_member_id()
        self.assertEquals(self.members.account.adapter.called, 0)

    def test_can_change_status_of_members_in_bulk2(self):
        # Setup
        MockAdapter.expected = False
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'status': member_status.Active
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'status': member_status.Active
            })
        }

        with self.assertRaises(MemberChangeStatusError):
            self.members.change_status_by_member_id([200, 201], member_status.OptOut)

        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'PUT',
            '/members/status',
            {'member_ids': [200, 201], 'status_to': u"o"}
        ))

    def test_can_change_status_of_members_in_bulk3(self):
        # Setup
        MockAdapter.expected = True
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'status': member_status.Active
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'status': member_status.Active
            })
        }

        self.members.change_status_by_member_id([200], member_status.OptOut)

        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'PUT',
            '/members/status',
            {'member_ids': [200], 'status_to': u"o"}
        ))
        self.assertEquals(2, len(self.members))
        self.assertEquals(member_status.OptOut, self.members[200]['status'])
        self.assertEquals(member_status.Active, self.members[201]['status'])

    def test_can_change_status_of_members_in_bulk4(self):
        # Setup
        MockAdapter.expected = True
        self.members._dict = {
            200: Member(self.members.account, {
                'member_id': 200,
                'email': u"test1@example.com",
                'status': member_status.Active
            }),
            201: Member(self.members.account, {
                'member_id': 201,
                'email': u"test2@example.com",
                'status': member_status.Active
            })
        }

        self.members.change_status_by_member_id([200, 201], member_status.OptOut)

        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'PUT',
            '/members/status',
            {'member_ids': [200, 201], 'status_to': u"o"}
            ))
        self.assertEquals(2, len(self.members))
        self.assertEquals(member_status.OptOut, self.members[200]['status'])
        self.assertEquals(member_status.OptOut, self.members[201]['status'])

    def test_can_change_status_of_members_in_bulk5(self):
        MockAdapter.expected = False

        with self.assertRaises(MemberChangeStatusError):
            self.members.change_status_by_status(
                member_status.Error,
                member_status.Active)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call,
            ('PUT', '/members/status/e/to/a', {}))

    def test_can_change_status_of_members_in_bulk6(self):
        MockAdapter.expected = True
        result = self.members.change_status_by_status(
            member_status.Error,
            member_status.Active)
        self.assertIsNone(result)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call,
            ('PUT', '/members/status/e/to/a', {}))

    def test_can_change_status_of_members_in_bulk7(self):
        MockAdapter.expected = True

        result = self.members.change_status_by_status(
            member_status.Error,
            member_status.Active,
            200)
        self.assertIsNone(result)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call,
            ('PUT', '/members/status/e/to/a', {'group_id': 200}))

    def test_can_drop_groups_of_members_in_bulk(self):
        self.members.drop_groups()
        self.assertEquals(self.members.account.adapter.called, 0)

    def test_can_drop_groups_of_members_in_bulk2(self):
        self.members.drop_groups([123, 321])
        self.assertEquals(self.members.account.adapter.called, 0)

    def test_can_drop_groups_of_members_in_bulk3(self):
        self.members.drop_groups([], [1024, 1025])
        self.assertEquals(self.members.account.adapter.called, 0)

    def test_can_drop_groups_of_members_in_bulk4(self):
        MockAdapter.expected = False

        with self.assertRaises(MemberDropGroupError):
            self.members.drop_groups([123, 321], [1024, 1025])

        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'PUT',
            '/members/groups/remove',
            {'member_ids': [123, 321], 'group_ids': [1024, 1025]}
        ))

    def test_can_drop_groups_of_members_in_bulk5(self):
        MockAdapter.expected = True

        result = self.members.drop_groups([123, 321], [1024, 1025])

        self.assertIsNone(result)
        self.assertEquals(self.members.account.adapter.called, 1)
        self.assertEquals(self.members.account.adapter.call, (
            'PUT',
            '/members/groups/remove',
            {'member_ids': [123, 321], 'group_ids': [1024, 1025]}
        ))
