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
    """Represents a logical AND"""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '["and", %s, %s]' % (self.left, self.right)


class DisjunctionQuery(CompositeQuery):
    """Represents a logical OR"""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '["or", %s, %s]' % (self.left, self.right)


class NegationQuery(CompositeQuery):
    """Represents a logical NOT"""
    def __init__(self, query):
        self.query = query

    def __str__(self):
        return '["not", %s]' % self.query