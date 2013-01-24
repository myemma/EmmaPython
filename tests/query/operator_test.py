import unittest
import myemma.query.operator as op
from myemma.query.factory import QueryFactory as q


class EqualityQueryTest(unittest.TestCase):
    def test_can_build_a_simple_equality_query(self):
        query = op.EqualityQuery('member_field:some_string_field', 'bar')
        self.assertTupleEqual(
            ("member_field:some_string_field", "eq", "bar"),
            query.to_tuple())

    def test_can_build_a_simple_equality_query2(self):
        query = q.eq('first_name', 'Test')
        self.assertIsInstance(query, op.EqualityQuery)
        self.assertTupleEqual(
            ("first_name", "eq", "Test"),
            query.to_tuple())


class LessThanQueryTest(unittest.TestCase):
    def test_can_build_a_simple_less_than_query(self):
        query = op.LessThanQuery('member_field:some_numeric_field', 5)
        self.assertTupleEqual(
            ("member_field:some_numeric_field", "lt", 5),
            query.to_tuple())

    def test_can_build_a_simple_less_than_query2(self):
        query = q.lt('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, op.LessThanQuery)
        self.assertTupleEqual(
            ("member_field:some_numeric_field", "lt", 5),
            query.to_tuple())


class GreaterThanQueryTest(unittest.TestCase):
    def test_can_build_a_simple_greater_than_query(self):
        query = op.GreaterThanQuery('member_field:some_numeric_field', 5)
        self.assertTupleEqual(
            ("member_field:some_numeric_field", "gt", 5),
            query.to_tuple())

    def test_can_build_a_simple_greater_than_query2(self):
        query = q.gt('member_field:some_numeric_field', 5)
        self.assertIsInstance(query, op.GreaterThanQuery)
        self.assertTupleEqual(
            ("member_field:some_numeric_field", "gt", 5),
            query.to_tuple())


class BetweenQueryTest(unittest.TestCase):
    def test_can_build_a_simple_between_query(self):
        query = op.BetweenQuery('member_field:some_numeric_field', 5, 10)
        self.assertTupleEqual(
            ("member_field:some_numeric_field", "between", 5, 10),
            query.to_tuple())

    def test_can_build_a_simple_between_query2(self):
        query = q.between('member_field:some_numeric_field', 5, 10)
        self.assertIsInstance(query, op.BetweenQuery)
        self.assertTupleEqual(
            ("member_field:some_numeric_field", "between", 5, 10),
            query.to_tuple())


class InLastQueryTest(unittest.TestCase):
    def test_can_build_a_simple_in_last_query(self):
        query = op.InLastQuery('member_since', {"day": 4})
        self.assertTupleEqual(
            ("member_since", "in last", {"day": 4}),
            query.to_tuple())

    def test_can_build_a_simple_in_last_query2(self):
        query = q.in_last('member_since', {"day": 4})
        self.assertIsInstance(query, op.InLastQuery)
        self.assertTupleEqual(
            ("member_since", "in last", {"day": 4}),
            query.to_tuple())


class InNextQueryTest(unittest.TestCase):
    def test_can_build_a_simple_in_next_query(self):
        query = op.InNextQuery('member_since', {"day": 4})
        self.assertTupleEqual(
            ("member_since", "in next", {"day": 4}),
            query.to_tuple())

    def test_can_build_a_simple_in_next_query2(self):
        query = q.in_next('member_since', {"day": 4})
        self.assertIsInstance(query, op.InNextQuery)
        self.assertTupleEqual(
            ("member_since", "in next", {"day": 4}),
            query.to_tuple())


class DateMatchQueryTest(unittest.TestCase):
    def test_can_build_a_simple_datematch_query(self):
        query = op.DateMatchQuery('member_since', {"year": 2011})
        self.assertTupleEqual(
            ("member_since", "datematch", {"year": 2011}),
            query.to_tuple())

    def test_can_build_a_simple_datematch_query2(self):
        query = q.datematch('member_since', {"year": 2011})
        self.assertIsInstance(query, op.DateMatchQuery)
        self.assertTupleEqual(
            ("member_since", "datematch", {"year": 2011}),
            query.to_tuple())


class ContainsQueryTest(unittest.TestCase):
    def test_can_build_a_simple_contains_query(self):
        query = op.ContainsQuery('member_field:some_string_field', '*foo*')
        self.assertTupleEqual(
            ("member_field:some_string_field", "contains", "*foo*"),
            query.to_tuple())

    def test_can_build_a_simple_contains_query2(self):
        query = q.contains('member_field:some_string_field', '*foo*')
        self.assertIsInstance(query, op.ContainsQuery)
        self.assertTupleEqual(
            ("member_field:some_string_field", "contains", "*foo*"),
            query.to_tuple())


class IsInQueryTest(unittest.TestCase):
    def test_can_build_a_simple_contains_query(self):
        query = op.IsInQuery('member_field:some_number_field', [3, 4, 5, 6])
        self.assertTupleEqual(
            ("member_field:some_number_field", "in", 3, 4, 5, 6),
            query.to_tuple())

    def test_can_build_a_simple_contains_query2(self):
        query = q.is_in('member_field:some_number_field', [3, 4, 5, 6])
        self.assertIsInstance(query, op.IsInQuery)
        self.assertTupleEqual(
            ("member_field:some_number_field", "in", 3, 4, 5, 6),
            query.to_tuple())


class AnyQueryTest(unittest.TestCase):
    def test_can_build_a_simple_any_query(self):
        query = op.AnyQuery('member_field:some_array_field', 'ten')
        self.assertTupleEqual(
            ("member_field:some_array_field", "any", "ten"),
            query.to_tuple())

    def test_can_build_a_simple_any_query2(self):
        query = q.any('member_field:some_array_field', 'ten')
        self.assertIsInstance(query, op.AnyQuery)
        self.assertTupleEqual(
            ("member_field:some_array_field", "any", "ten"),
            query.to_tuple())


class ZipRadiusQueryTest(unittest.TestCase):
    def test_can_build_a_simple_contains_query(self):
        query = op.ZipRadiusQuery('member_field:some_zipcode_field', 10, 97202)
        self.assertTupleEqual(
            ("member_field:some_zipcode_field", "zip-radius:10", "97202"),
            query.to_tuple())

    def test_can_build_a_simple_contains_query2(self):
        query = q.zip_radius('member_field:some_zipcode_field', 10, 97202)
        self.assertIsInstance(query, op.ZipRadiusQuery)
        self.assertTupleEqual(
            ("member_field:some_zipcode_field", "zip-radius:10", "97202"),
            query.to_tuple())

    def test_can_build_a_simple_contains_query3(self):
        with self.assertRaises(Exception):
            q.zip_radius('member_field:some_zipcode_field', 22, 97202)

