import unittest
from myemma.model.member import Member, MemberGroupCollection, MemberMailingCollection, NoMemberIdError, NoMemberStatusError, NoMemberEmailError
from myemma.model.group import Group
from myemma.model.mailing import Mailing

class MockAdapter(object):
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

class MemberTest(unittest.TestCase):
    def setUp(self):
        self.member = Member(
            MockAdapter(),
            {
                u"member_id":1000,
                u"email":u"test@example.com",
                u"status":u"opt-out"
            }
        )

    def test_group_collection_can_be_accessed(self):
        self.assertIsInstance(self.member.groups, MemberGroupCollection)

    def test_mailing_collection_can_be_accessed(self):
        self.assertIsInstance(self.member.mailings, MemberMailingCollection)

    def test_can_get_opt_out_detail_for_member(self):
        MockAdapter.expected = []
        detail = self.member.get_opt_out_detail()
        self.assertIsInstance(detail, list)
        self.assertEquals(self.member.adapter.called, 1)
        self.assertEquals(
            self.member.adapter.call,
            ('GET', '/members/1000/optout', {}))

    def test_can_get_opt_out_detail_for_member2(self):
        MockAdapter.expected = []
        member = Member(MockAdapter())
        with self.assertRaises(NoMemberIdError):
            member.get_opt_out_detail()
        self.assertEquals(member.adapter.called, 0)

    def test_can_ask_if_member_has_opted_out(self):
        has_opted_out = self.member.has_opted_out()
        self.assertIsInstance(has_opted_out, bool)
        self.assertTrue(has_opted_out)
        self.assertEquals(self.member.adapter.called, 0)

    def test_can_ask_if_member_has_opted_out2(self):
        member = Member(
            MockAdapter(),
            {
                u"member_id":1000,
                u"email":u"test@example.com",
                u"status":u"active"
            }
        )
        has_opted_out = member.has_opted_out()
        self.assertIsInstance(has_opted_out, bool)
        self.assertFalse(has_opted_out)
        self.assertEquals(member.adapter.called, 0)

    def test_can_ask_if_member_has_opted_out3(self):
        member = Member(MockAdapter())
        with self.assertRaises(NoMemberStatusError):
            member.has_opted_out()
        self.assertEquals(member.adapter.called, 0)

    def test_can_opt_out_a_member(self):
        member = Member(MockAdapter())
        with self.assertRaises(NoMemberEmailError):
            member.opt_out()
        self.assertEquals(member.adapter.called, 0)

    def test_can_opt_out_a_member2(self):
        member = Member(
            MockAdapter(),
            {
                u"member_id":1000,
                u"email":u"test@example.com",
                u"status":u"active"
            }
        )
        MockAdapter.expected = True
        self.assertFalse(member.has_opted_out())
        result = member.opt_out()
        self.assertIsNone(result)
        self.assertEquals(member.adapter.called, 1)
        self.assertEquals(
            member.adapter.call,
            ('PUT', '/members/email/optout/test@example.com', {}))
        self.assertTrue(member.has_opted_out())


class MemberGroupCollectionTest(unittest.TestCase):
    def setUp(self):
        adapter = MockAdapter()
        member = Member(adapter, {u"member_id":1000, u"email":u"test@example.com"})
        self.groups = MemberGroupCollection(adapter, member)

    def test_fetch_all_returns_a_dictionary(self):
        adapter = MockAdapter()
        groups = MemberGroupCollection(adapter, Member(adapter))
        with self.assertRaises(NoMemberIdError):
            groups.fetch_all()
        self.assertEquals(groups.adapter.called, 0)

    def test_fetch_all_returns_a_dictionary2(self):
        MockAdapter.expected = [{u"group_name": u"Test Group"}]
        self.assertIsInstance(self.groups.fetch_all(), dict)
        self.assertEquals(self.groups.adapter.called, 1)
        self.assertEquals(
            self.groups.adapter.call,
            ('GET', '/members/1000/groups', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{u"group_name": u"Test Group"}]
        self.assertEquals(0, len(self.groups))
        self.groups.fetch_all()
        self.assertEquals(1, len(self.groups))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{u"group_name": u"Test Group"}]
        self.groups.fetch_all()
        self.groups.fetch_all()
        self.assertEquals(self.groups.adapter.called, 1)

    def test_collection_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{u"group_name": u"Test Group"}]
        self.groups.fetch_all()
        self.assertIsInstance(self.groups, MemberGroupCollection)
        self.assertEquals(1, len(self.groups))
        self.assertIsInstance(self.groups[u"Test Group"], Group)

class MemberMailingCollectionTest(unittest.TestCase):
    def setUp(self):
        adapter = MockAdapter()
        member = Member(adapter, {u"member_id":1000, u"email":u"test@example.com"})
        self.mailings = MemberMailingCollection(adapter, member)

    def test_fetch_all_returns_a_dictionary(self):
        adapter = MockAdapter()
        mailings = MemberMailingCollection(adapter, Member(adapter))
        with self.assertRaises(NoMemberIdError):
            mailings.fetch_all()
        self.assertEquals(mailings.adapter.called, 0)

    def test_fetch_all_returns_a_dictionary2(self):
        MockAdapter.expected = [{u"mailing_id": 201}]
        self.assertIsInstance(self.mailings.fetch_all(), dict)
        self.assertEquals(self.mailings.adapter.called, 1)
        self.assertEquals(
            self.mailings.adapter.call,
            ('GET', '/members/1000/mailings', {}))

    def test_fetch_all_populates_collection(self):
        MockAdapter.expected = [{u"mailing_id": 201}]
        self.assertEquals(0, len(self.mailings))
        self.mailings.fetch_all()
        self.assertEquals(1, len(self.mailings))

    def test_fetch_all_caches_results(self):
        MockAdapter.expected = [{u"mailing_id": 201}]
        self.mailings.fetch_all()
        self.mailings.fetch_all()
        self.assertEquals(self.mailings.adapter.called, 1)

    def test_collection_can_be_accessed_like_a_dictionary(self):
        MockAdapter.expected = [{u"mailing_id": 201}]
        self.mailings.fetch_all()
        self.assertIsInstance(self.mailings, MemberMailingCollection)
        self.assertEquals(1, len(self.mailings))
        self.assertIsInstance(self.mailings[201], Mailing)
