"""Emma search syntax operators"""

from myemma.query.spec import CompositeQuery


class EqualityQuery(CompositeQuery):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "eq", "%s"]' % (self.field, self.value)


class LessThanQuery(CompositeQuery):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "lt", %s]' % (self.field, self.value)


class GreaterThanQuery(CompositeQuery):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "gt", %s]' % (self.field, self.value)


class BetweenQuery(CompositeQuery):
    def __init__(self, field, low, high):
        self.field = field
        self.low = low
        self.high = high

    def __str__(self):
        return '["%s", "between", %s, %s]' % (self.field, self.low, self.high)


class InLastQuery(CompositeQuery):
    pass


class InNextQuery(CompositeQuery):
    pass


class DateMatchQuery(CompositeQuery):
    pass


class ContainsQuery(CompositeQuery):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "contains", "%s"]' % (self.field, self.value)


class AnyQuery(CompositeQuery):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "any", "%s"]' % (self.field, self.value)


class ZipRadiusQuery(CompositeQuery):
    pass
