__all__ = ['CompositeQuery', 'ConjunctionQuery', 'DisjunctionQuery',
           'NegationQuery']

class CompositeQuery(object):
    def conjoin(self, other):
        return ConjunctionQuery(self, other)
    def __and__(self, other):
        return self.conjoin(other)

    def disjoin(self, other):
        return DisjunctionQuery(self, other)
    def __or__(self, other):
        return self.disjoin(other)

    def negate(self):
        return NegationQuery(self)
    def __invert__(self):
        return self.negate()

class ConjunctionQuery(CompositeQuery):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '["and", %s, %s]' % (self.left, self.right)

class DisjunctionQuery(CompositeQuery):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '["or", %s, %s]' % (self.left, self.right)

class NegationQuery(CompositeQuery):
    def __init__(self, query):
        self.query = query

    def __str__(self):
        return '["not", %s]' % self.query