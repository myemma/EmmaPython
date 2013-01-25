"""A simple implementation of the specification patter"""

class CompositeQuery(object):
    """Base class for the specification"""
    def conjoin(self, other):
        """ConjunctionQuery factory"""
        return ConjunctionQuery(self, other)
    def __and__(self, other):
        return self.conjoin(other)

    def disjoin(self, other):
        """DisjunctionQuery factory"""
        return DisjunctionQuery(self, other)
    def __or__(self, other):
        return self.disjoin(other)

    def negate(self):
        """NegationQuery factory"""
        return NegationQuery(self)
    def __invert__(self):
        return self.negate()


class ConjunctionQuery(CompositeQuery):
    """Represents a logical conjunction (AND)"""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_tuple(self):
        return "and", self.left.to_tuple(), self.right.to_tuple()


class DisjunctionQuery(CompositeQuery):
    """Represents a logical disjunction (OR)"""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_tuple(self):
        return "or", self.left.to_tuple(), self.right.to_tuple()


class NegationQuery(CompositeQuery):
    """Represents a logical negation (NOT)"""
    def __init__(self, query):
        self.query = query

    def to_tuple(self):
        return "not", self.query.to_tuple()