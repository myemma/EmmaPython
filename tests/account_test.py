import unittest
from myemma.adapter import AbstractAdapter
from myemma.adapter.requests_adapter import RequestsAdapter
from myemma.model.account import Account, FieldCollection, ImportCollection, MemberCollection
from myemma.model.field import Field
from myemma.model.emma_import import EmmaImport
from myemma.model.member import Member

class MockAdapter(AbstractAdapter):
    expected = None

    def __init__(self, *args, **kwargs):
        self.called = 0
        self.call = ()

    def _capture(self, method, path, params):
        self.called += 1
        self.call = (method, path, params)

    def get(self, path, params={}):
        self._capture('GET', path, params)
        return self.__class__.expected

    def post(self, path, params={}):
        self._capture('POST', path, params)
        return self.__class__.expected

    def put(self, path, params={}):
        self._capture('PUT', path, params)
        return self.__class__.expected

    def delete(self, path, params={}):
        self._capture('DELETE', path, params)
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
        self.assertIsInstance(self.account.fields, FieldCollection)

    def test_import_collection_can_be_accessed(self):
        self.assertIsInstance(self.account.imports, ImportCollection)

    def test_member_collection_can_be_accessed(self):
        self.assertIsInstance(self.account.members, MemberCollection)

class FieldCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.fields = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy").fields

    def test_fetch_all_returns_a_dictionary(self):
        MockAdapter.expected = [{u"field_id": 201}]
        self.assertIsInstance(self.fields.fetch_all(), dict)
        self.assertEquals(self.fields.adapter.called, 1)
        self.assertEquals(
            self.fields.adapter.call,
            ('GET', '/fields', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{u"field_id": 201}]
        self.assertEquals(0, len(self.fields))
        self.fields.fetch_all()
        self.assertEquals(1, len(self.fields))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{u"field_id": 201}]
        self.fields.fetch_all()
        self.fields.fetch_all()
        self.assertEquals(self.fields.adapter.called, 1)

    def test_field_collection_object_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{u"field_id": 201}]
        self.fields.fetch_all()
        self.assertIsInstance(self.fields, FieldCollection)
        self.assertEquals(1, len(self.fields))
        self.assertIsInstance(self.fields[201], Field)

class ImportCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.imports = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy").imports

    def test_fetch_all_returns_a_dictionary(self):
        MockAdapter.expected = [{u"import_id": 201}]
        self.assertIsInstance(self.imports.fetch_all(), dict)
        self.assertEquals(self.imports.adapter.called, 1)
        self.assertEquals(
            self.imports.adapter.call,
            ('GET', '/members/imports', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{u"import_id": 201}]
        self.assertEquals(0, len(self.imports))
        self.imports.fetch_all()
        self.assertEquals(1, len(self.imports))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{u"import_id": 201}]
        self.imports.fetch_all()
        self.imports.fetch_all()
        self.assertEquals(self.imports.adapter.called, 1)

    def test_imports_collection_object_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{u"import_id": 201}]
        self.imports.fetch_all()
        self.assertIsInstance(self.imports, ImportCollection)
        self.assertEquals(1, len(self.imports))
        self.assertIsInstance(self.imports[201], EmmaImport)

    def test_fetch_one_by_import_id_returns_an_import_object(self):
        MockAdapter.expected = {u"import_id": 201}
        emma_import = self.imports.find_one_by_import_id(201)
        self.assertIsInstance(emma_import, EmmaImport)
        self.assertEquals(emma_import[u"import_id"], 201)
        self.assertEquals(self.imports.adapter.called, 1)
        self.assertEquals(
            self.imports.adapter.call,
            ('GET', '/members/imports/201', {}))

    def test_fetch_one_by_import_id_populates_collection(self):
        MockAdapter.expected = {u"import_id": 201}
        self.imports.find_one_by_import_id(201)
        self.assertIn(201, self.imports)
        self.assertIsInstance(self.imports[201], EmmaImport)
        self.assertEquals(self.imports[201][u"import_id"], 201)

    def test_fetch_one_by_import_id_caches_result(self):
        MockAdapter.expected = {u"import_id": 201}
        self.imports.find_one_by_import_id(201)
        self.imports.find_one_by_import_id(201)
        self.assertEquals(self.imports.adapter.called, 1)

    def test_dictionary_access_lazy_loads_by_import_id(self):
        MockAdapter.expected = {u"import_id": 201}
        emma_import = self.imports[201]
        self.assertIn(201, self.imports)
        self.assertIsInstance(emma_import, EmmaImport)
        self.assertEquals(self.imports[201][u"import_id"], 201)
        self.assertEquals(self.imports.adapter.called, 1)
        self.assertEquals(
            self.imports.adapter.call,
            ('GET', '/members/imports/201', {}))

    def test_dictionary_access_lazy_loads_by_import_id2(self):
        MockAdapter.expected = None
        emma_import = self.imports[204]
        self.assertEquals(0, len(self.imports))
        self.assertIsNone(emma_import)
        self.assertEquals(self.imports.adapter.called, 1)
        self.assertEquals(
            self.imports.adapter.call,
            ('GET', '/members/imports/204', {}))

class MemberCollectionTest(unittest.TestCase):
    def setUp(self):
        Account.default_adapter = MockAdapter
        self.members = Account(
            account_id="100",
            public_key="xxx",
            private_key="yyy").members

    def test_fetch_all_returns_a_dictionary(self):
        MockAdapter.expected = [{u"member_id": 201}]
        self.assertIsInstance(self.members.fetch_all(), dict)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members', {}))

    def test_fetch_all_returns_a_dictionary2(self):
        MockAdapter.expected = [{u"member_id": 201},{u"member_id": 204}]
        self.assertIsInstance(self.members.fetch_all(deleted=True), dict)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members', {"deleted":True}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{u"member_id": 201}]
        self.assertEquals(0, len(self.members))
        self.members.fetch_all()
        self.assertEquals(1, len(self.members))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{u"member_id": 201}]
        self.members.fetch_all()
        self.members.fetch_all()
        self.assertEquals(self.members.adapter.called, 1)

    def test_members_collection_object_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{u"member_id": 201}]
        self.members.fetch_all()
        self.assertIsInstance(self.members, MemberCollection)
        self.assertEquals(1, len(self.members))
        self.assertIsInstance(self.members[201], Member)

    def test_fetch_all_by_import_id_returns_a_dictionary(self):
        MockAdapter.expected = [{u"member_id": 201}]
        self.assertIsInstance(self.members.fetch_all_by_import_id(100), dict)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/imports/100/members', {}))

    def test_fetch_all_by_import_id_updates_collection(self):
        MockAdapter.expected = [{u"member_id": 201}]
        self.assertEquals(0, len(self.members))
        self.members.fetch_all_by_import_id(100)
        self.assertEquals(1, len(self.members))

    def test_fetch_all_by_import_id_does_not_cache_results(self):
        MockAdapter.expected = [{u"member_id": 201}]
        self.members.fetch_all_by_import_id(100)
        self.members.fetch_all_by_import_id(100)
        self.assertEquals(self.members.adapter.called, 2)

    def test_fetch_one_by_member_id_returns_a_member_object(self):
        MockAdapter.expected = {u"member_id": 201}
        member = self.members.find_one_by_member_id(201)
        self.assertIsInstance(member, Member)
        self.assertEquals(member[u"member_id"], 201)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/201', {}))

    def test_fetch_one_by_member_id_returns_a_member_object2(self):
        MockAdapter.expected = {u"member_id": 204}
        member = self.members.find_one_by_member_id(204, deleted=True)
        self.assertIsInstance(member, Member)
        self.assertEquals(member[u"member_id"], 204)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/204', {"deleted":True}))

    def test_fetch_one_by_member_id_populates_collection(self):
        MockAdapter.expected = {u"member_id": 201}
        self.members.find_one_by_member_id(201)
        self.assertIn(201, self.members)
        self.assertIsInstance(self.members[201], Member)
        self.assertEquals(self.members[201][u"member_id"], 201)

    def test_fetch_one_by_member_id_caches_result(self):
        MockAdapter.expected = {u"member_id": 201}
        self.members.find_one_by_member_id(201)
        self.members.find_one_by_member_id(201)
        self.assertEquals(self.members.adapter.called, 1)

    def test_dictionary_access_lazy_loads_by_member_id(self):
        MockAdapter.expected = {u"member_id": 201}
        member = self.members[201]
        self.assertIn(201, self.members)
        self.assertIsInstance(member, Member)
        self.assertEquals(self.members[201][u"member_id"], 201)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/201', {}))

    def test_dictionary_access_lazy_loads_by_member_id2(self):
        MockAdapter.expected = None
        member = self.members[204]
        self.assertEquals(0, len(self.members))
        self.assertIsNone(member)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/204', {}))

    def test_fetch_one_by_email_returns_a_member_object(self):
        MockAdapter.expected = {u"member_id": 201, u"email": u"test@example.com"}
        member = self.members.find_one_by_email("test@example.com")
        self.assertIsInstance(member, Member)
        self.assertEquals(member[u"member_id"], 201)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_fetch_one_by_email_returns_a_member_object2(self):
        MockAdapter.expected = {u"member_id": 204, u"email": u"test@example.com"}
        member = self.members.find_one_by_email("test@example.com", deleted=True)
        self.assertIsInstance(member, Member)
        self.assertEquals(member[u"member_id"], 204)
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/email/test@example.com', {"deleted":True}))

    def test_fetch_one_by_email_populates_collection(self):
        MockAdapter.expected = {u"member_id": 201, u"email": u"test@example.com"}
        self.members.find_one_by_email("test@example.com")
        self.assertIn(201, self.members)
        self.assertIsInstance(self.members[201], Member)
        self.assertEquals(self.members[201][u"member_id"], 201)

    def test_fetch_one_by_email_caches_result(self):
        MockAdapter.expected = {u"member_id": 201, u"email": u"test@example.com"}
        self.members.find_one_by_email("test@example.com")
        self.members.find_one_by_email("test@example.com")
        self.assertEquals(self.members.adapter.called, 1)

    def test_dictionary_access_lazy_loads_by_email(self):
        MockAdapter.expected = {u"member_id": 201, u"email": u"test@example.com"}
        member = self.members["test@example.com"]
        self.assertIn(201, self.members)
        self.assertIsInstance(member, Member)
        self.assertEquals(self.members[201][u"member_id"], 201)
        self.assertEquals(self.members[201][u"email"], u"test@example.com")
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_dictionary_access_lazy_loads_by_email2(self):
        MockAdapter.expected = {u"member_id": 201, u"email": u"test@example.com"}
        member = self.members[u"test@example.com"]
        self.assertIn(201, self.members)
        self.assertIsInstance(member, Member)
        self.assertEquals(self.members[201][u"member_id"], 201)
        self.assertEquals(self.members[201][u"email"], u"test@example.com")
        self.assertEquals(self.members.adapter.called, 1)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_dictionary_access_lazy_loads_by_email3(self):
        MockAdapter.expected = None
        member = self.members["test@example.com"]
        self.assertEquals(0, len(self.members))
        self.assertIsNone(member)
        self.assertEquals(1, self.members.adapter.called)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/email/test@example.com', {}))

    def test_dictionary_access_lazy_loads_by_email4(self):
        MockAdapter.expected = None
        member = self.members[u"test@example.com"]
        self.assertEquals(0, len(self.members))
        self.assertIsNone(member)
        self.assertEquals(1, self.members.adapter.called)
        self.assertEquals(
            self.members.adapter.call,
            ('GET', '/members/email/test@example.com', {}))
