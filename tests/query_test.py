import unittest

from myemma.query import *
from myemma.query.factory import QueryFactory as q

class EqualityQueryTest(unittest.TestCase):

    def test_can_build_a_simple_equality_query(self):
        query = EqualityQuery('member_field:some_string_field', 'bar')
        self.assertIsInstance(query, EqualityQuery)
        self.assertEquals('["member_field:some_string_field", "eq", "bar"]', "%s" % query)

    def test_can_build_a_simple_equality_query2(self):
        query = q.eq('first_name', 'Test')
        self.assertIsInstance(query, EqualityQuery)
        self.assertEquals('["first_name", "eq", "Test"]', "%s" % query)

    def test_can_build_a_simple_less_than_query(self):
        query = LessThanQuery('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, LessThanQuery)
        self.assertEquals('["member_field:some_numeric_field", "lt", 5]', "%s" % query)

    def test_can_build_a_simple_less_than_query2(self):
        query = q.lt('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, LessThanQuery)
        self.assertEquals('["member_field:some_numeric_field", "lt", 5]', "%s" % query)

    def test_can_build_a_simple_greater_than_query(self):
        query = GreaterThanQuery('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, GreaterThanQuery)
        self.assertEquals('["member_field:some_numeric_field", "gt", 5]', "%s" % query)

    def test_can_build_a_simple_greater_than_query2(self):
        query = q.gt('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, GreaterThanQuery)
        self.assertEquals('["member_field:some_numeric_field", "gt", 5]', "%s" % query)

    def test_can_build_a_simple_between_query(self):
        query = BetweenQuery('member_field:some_numeric_field', 5, 10)
        self.assertIsInstance(query, BetweenQuery)
        self.assertEquals('["member_field:some_numeric_field", "between", 5, 10]', "%s" % query)

    def test_can_build_a_simple_between_query2(self):
        query = q.between('member_field:some_numeric_field', 5, 10)
        self.assertIsInstance(query, BetweenQuery)
        self.assertEquals('["member_field:some_numeric_field", "between", 5, 10]', "%s" % query)

    def test_can_build_a_simple_contains_query(self):
        query = ContainsQuery('member_field:some_string_field', '*foo*')
        self.assertIsInstance(query, ContainsQuery)
        self.assertEquals('["member_field:some_string_field", "contains", "*foo*"]', "%s" % query)

    def test_can_build_a_simple_contains_query(self):
        query = q.contains('member_field:some_string_field', '*foo*')
        self.assertIsInstance(query, ContainsQuery)
        self.assertEquals('["member_field:some_string_field", "contains", "*foo*"]', "%s" % query)

    def test_can_build_a_simple_any_query(self):
        query = AnyQuery('member_field:some_array_field', 'ten')
        self.assertIsInstance(query, AnyQuery)
        self.assertEquals('["member_field:some_array_field", "any", "ten"]', "%s" % query)

    def test_can_build_a_simple_any_query(self):
        query = q.any('member_field:some_array_field', 'ten')
        self.assertIsInstance(query, AnyQuery)
        self.assertEquals('["member_field:some_array_field", "any", "ten"]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_conjunction(self):
        query = q.eq('first_name', 'TestFirst').conjoin(q.eq('last_name', 'TestLast'))
        self.assertIsInstance(query, ConjunctionQuery)
        self.assertEquals('["and", ["first_name", "eq", "TestFirst"], ["last_name", "eq", "TestLast"]]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_conjunction2(self):
        query = q.eq('first_name', 'TestFirst') & q.eq('last_name', 'TestLast')
        self.assertIsInstance(query, ConjunctionQuery)
        self.assertEquals('["and", ["first_name", "eq", "TestFirst"], ["last_name", "eq", "TestLast"]]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_conjunction3(self):
        query = q.eq('first_name', 'TestFirst')
        query &= q.eq('last_name', 'TestLast')
        self.assertIsInstance(query, ConjunctionQuery)
        self.assertEquals('["and", ["first_name", "eq", "TestFirst"], ["last_name", "eq", "TestLast"]]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_disjunction(self):
        query = q.eq('first_name', 'TestFirst').disjoin(q.eq('last_name', 'TestLast'))
        self.assertIsInstance(query, DisjunctionQuery)
        self.assertEquals('["or", ["first_name", "eq", "TestFirst"], ["last_name", "eq", "TestLast"]]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_disjunction2(self):
        query = q.eq('first_name', 'TestFirst') | q.eq('last_name', 'TestLast')
        self.assertIsInstance(query, DisjunctionQuery)
        self.assertEquals('["or", ["first_name", "eq", "TestFirst"], ["last_name", "eq", "TestLast"]]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_disjunction3(self):
        query = q.eq('first_name', 'TestFirst')
        query |= q.eq('last_name', 'TestLast')
        self.assertIsInstance(query, DisjunctionQuery)
        self.assertEquals('["or", ["first_name", "eq", "TestFirst"], ["last_name", "eq", "TestLast"]]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_Negation(self):
        query = q.eq('first_name', 'TestFirst').negate()
        self.assertIsInstance(query, NegationQuery)
        self.assertEquals('["not", ["first_name", "eq", "TestFirst"]]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_Negation2(self):
        query = ~ q.eq('first_name', 'TestFirst')
        self.assertIsInstance(query, NegationQuery)
        self.assertEquals('["not", ["first_name", "eq", "TestFirst"]]', "%s" % query)

    def test_can_build_a_complex_equality_query_using_Negation3(self):
        query = q.eq('first_name', 'TestFirst')
        query = ~ query
        self.assertIsInstance(query, NegationQuery)
        self.assertEquals('["not", ["first_name", "eq", "TestFirst"]]', "%s" % query)
