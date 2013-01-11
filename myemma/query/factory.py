from operator import *

class QueryFactory(object):
    @staticmethod
    def eq(field, value): return EqualityQuery(field, value)
    @staticmethod
    def lt(field, value): return LessThanQuery(field, value)
    @staticmethod
    def gt(field, value): return GreaterThanQuery(field, value)
    @staticmethod
    def between(field, low, high): return BetweenQuery(field, low, high)
    @staticmethod
    def contains(field, value): return ContainsQuery(field, value)
    @staticmethod
    def any(field, value): return AnyQuery(field, value)
