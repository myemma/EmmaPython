import unittest
import myemma.query.operator as op
from myemma.query.factory import QueryFactory as q


class EqualityQueryTest(unittest.TestCase):
    def test_can_build_a_simple_equality_query(self):
        query = op.EqualityQuery('member_field:some_string_field', 'bar')
        self.assertIsInstance(query, op.EqualityQuery)
        self.assertEquals('["member_field:some_string_field", "eq", "bar"]', "%s" % query)

    def test_can_build_a_simple_equality_query2(self):
        query = q.eq('first_name', 'Test')
        self.assertIsInstance(query, op.EqualityQuery)
        self.assertEquals('["first_name", "eq", "Test"]', "%s" % query)


class LessThanQueryTest(unittest.TestCase):
    def test_can_build_a_simple_less_than_query(self):
        query = op.LessThanQuery('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, op.LessThanQuery)
        self.assertEquals('["member_field:some_numeric_field", "lt", 5]', "%s" % query)

    def test_can_build_a_simple_less_than_query2(self):
        query = q.lt('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, op.LessThanQuery)
        self.assertEquals('["member_field:some_numeric_field", "lt", 5]', "%s" % query)


class GreaterThanQueryTest(unittest.TestCase):
    def test_can_build_a_simple_greater_than_query(self):
        query = op.GreaterThanQuery('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, op.GreaterThanQuery)
        self.assertEquals('["member_field:some_numeric_field", "gt", 5]', "%s" % query)

    def test_can_build_a_simple_greater_than_query2(self):
        query = q.gt('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, op.GreaterThanQuery)
        self.assertEquals('["member_field:some_numeric_field", "gt", 5]', "%s" % query)


class BetweenQueryTest(unittest.TestCase):
    def test_can_build_a_simple_between_query(self):
        query = op.BetweenQuery('member_field:some_numeric_field', 5, 10)
        self.assertIsInstance(query, op.BetweenQuery)
        self.assertEquals('["member_field:some_numeric_field", "between", 5, 10]', "%s" % query)

    def test_can_build_a_simple_between_query2(self):
        query = q.between('member_field:some_numeric_field', 5, 10)
        self.assertIsInstance(query, op.BetweenQuery)
        self.assertEquals('["member_field:some_numeric_field", "between", 5, 10]', "%s" % query)


class ContainsQueryTest(unittest.TestCase):
    def test_can_build_a_simple_contains_query(self):
        query = op.ContainsQuery('member_field:some_string_field', '*foo*')
        self.assertIsInstance(query, op.ContainsQuery)
        self.assertEquals('["member_field:some_string_field", "contains", "*foo*"]', "%s" % query)

    def test_can_build_a_simple_contains_query(self):
        query = q.contains('member_field:some_string_field', '*foo*')
        self.assertIsInstance(query, op.ContainsQuery)
        self.assertEquals('["member_field:some_string_field", "contains", "*foo*"]', "%s" % query)


class AnyQueryTest(unittest.TestCase):
    def test_can_build_a_simple_any_query(self):
        query = op.AnyQuery('member_field:some_array_field', 'ten')
        self.assertIsInstance(query, op.AnyQuery)
        self.assertEquals('["member_field:some_array_field", "any", "ten"]', "%s" % query)

    def test_can_build_a_simple_any_query(self):
        query = q.any('member_field:some_array_field', 'ten')
        self.assertIsInstance(query, op.AnyQuery)
        self.assertEquals('["member_field:some_array_field", "any", "ten"]', "%s" % query)

