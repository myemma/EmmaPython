import unittest
from emma.query.spec import ConjunctionQuery, DisjunctionQuery, NegationQuery
from emma.query.factory import QueryFactory as q


class ConjunctionQueryTest(unittest.TestCase):
    def test_can_build_a_complex_equality_query_using_conjunction(self):
        query = q.eq('first_name', 'TestFirst').conjoin(q.eq('last_name', 'TestLast'))
        self.assertIsInstance(query, ConjunctionQuery)
        self.assertTupleEqual(
            ("and", ("first_name", "eq", "TestFirst"), ("last_name", "eq", "TestLast")),
            query.to_tuple())

    def test_can_build_a_complex_equality_query_using_conjunction2(self):
        query = q.eq('first_name', 'TestFirst') & q.eq('last_name', 'TestLast')
        self.assertIsInstance(query, ConjunctionQuery)
        self.assertTupleEqual(
            ("and", ("first_name", "eq", "TestFirst"), ("last_name", "eq", "TestLast")),
            query.to_tuple())

    def test_can_build_a_complex_equality_query_using_conjunction3(self):
        query = q.eq('first_name', 'TestFirst')
        query &= q.eq('last_name', 'TestLast')
        self.assertIsInstance(query, ConjunctionQuery)
        self.assertTupleEqual(
            ("and", ("first_name", "eq", "TestFirst"), ("last_name", "eq", "TestLast")),
            query.to_tuple())


class DisjunctionQueryTest(unittest.TestCase):
    def test_can_build_a_complex_equality_query_using_disjunction(self):
        query = q.eq('first_name', 'TestFirst').disjoin(q.eq('last_name', 'TestLast'))
        self.assertIsInstance(query, DisjunctionQuery)
        self.assertTupleEqual(
            ("or", ("first_name", "eq", "TestFirst"), ("last_name", "eq", "TestLast")),
            query.to_tuple())

    def test_can_build_a_complex_equality_query_using_disjunction2(self):
        query = q.eq('first_name', 'TestFirst') | q.eq('last_name', 'TestLast')
        self.assertIsInstance(query, DisjunctionQuery)
        self.assertTupleEqual(
            ("or", ("first_name", "eq", "TestFirst"), ("last_name", "eq", "TestLast")),
            query.to_tuple())

    def test_can_build_a_complex_equality_query_using_disjunction3(self):
        query = q.eq('first_name', 'TestFirst')
        query |= q.eq('last_name', 'TestLast')
        self.assertIsInstance(query, DisjunctionQuery)
        self.assertTupleEqual(
            ("or", ("first_name", "eq", "TestFirst"), ("last_name", "eq", "TestLast")),
            query.to_tuple())


class NegationQueryTest(unittest.TestCase):
    def test_can_build_a_complex_equality_query_using_Negation(self):
        query = q.eq('first_name', 'TestFirst').negate()
        self.assertIsInstance(query, NegationQuery)
        self.assertTupleEqual(
            ("not", ("first_name", "eq", "TestFirst")),
            query.to_tuple())

    def test_can_build_a_complex_equality_query_using_Negation2(self):
        query = ~ q.eq('first_name', 'TestFirst')
        self.assertIsInstance(query, NegationQuery)
        self.assertTupleEqual(
            ("not", ("first_name", "eq", "TestFirst")),
            query.to_tuple())

    def test_can_build_a_complex_equality_query_using_Negation3(self):
        query = q.eq('first_name', 'TestFirst')
        query = ~ query
        self.assertIsInstance(query, NegationQuery)
        self.assertTupleEqual(
            ("not", ("first_name", "eq", "TestFirst")),
            query.to_tuple())
