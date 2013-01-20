"""Emma search syntax operators"""

from myemma.query.spec import CompositeQuery


class EqualityQuery(CompositeQuery):
    """Basic equality"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "eq", "%s"]' % (self.field, self.value)


class LessThanQuery(CompositeQuery):
    """Less than"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "lt", %s]' % (self.field, self.value)


class GreaterThanQuery(CompositeQuery):
    """Greater than"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "gt", %s]' % (self.field, self.value)


class BetweenQuery(CompositeQuery):
    """Between"""
    def __init__(self, field, low, high):
        self.field = field
        self.low = low
        self.high = high

    def __str__(self):
        return '["%s", "between", %s, %s]' % (self.field, self.low, self.high)


class InLastQuery(CompositeQuery):
    """Relative date"""
    pass


class InNextQuery(CompositeQuery):
    """Relative date"""
    pass


class DateMatchQuery(CompositeQuery):
    """Match a date argument. All parts of the date must match."""
    pass


class ContainsQuery(CompositeQuery):
    """Match a string against a shell-glob-style expression"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "contains", "%s"]' % (self.field, self.value)


class AnyQuery(CompositeQuery):
    """Match a given value against an array field"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '["%s", "any", "%s"]' % (self.field, self.value)


class ZipRadiusQuery(CompositeQuery):
    """Takes a single zip code which will be the center of the search"""
    pass
