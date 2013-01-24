"""Emma search syntax operators"""

from myemma.query.spec import CompositeQuery


class EqualityQuery(CompositeQuery):
    """Basic equality"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def to_tuple(self):
        return self.field, "eq", self.value


class LessThanQuery(CompositeQuery):
    """Less than"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def to_tuple(self):
        return self.field, "lt", self.value


class GreaterThanQuery(CompositeQuery):
    """Greater than"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def to_tuple(self):
        return self.field, "gt", self.value


class BetweenQuery(CompositeQuery):
    """Between"""
    def __init__(self, field, low, high):
        self.field = field
        self.low = low
        self.high = high

    def to_tuple(self):
        return self.field, "between", self.low, self.high


class InLastQuery(CompositeQuery):
    """Relative date"""
    def __init__(self, field, interval):
        self.field = field
        self.interval = interval

    def to_tuple(self):
        return self.field, "in last", self.interval


class InNextQuery(CompositeQuery):
    """Relative date"""
    def __init__(self, field, interval):
        self.field = field
        self.interval = interval

    def to_tuple(self):
        return self.field, "in next", self.interval


class DateMatchQuery(CompositeQuery):
    """Match a date argument. All parts of the date must match."""
    def __init__(self, field, date):
        self.field = field
        self.date = date

    def to_tuple(self):
        return self.field, "datematch", self.date


class ContainsQuery(CompositeQuery):
    """Match a string against a shell-glob-style expression"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def to_tuple(self):
        return self.field, "contains", self.value


class AnyQuery(CompositeQuery):
    """Match a given value against an array field"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def to_tuple(self):
        return self.field, "any", self.value


class IsInQuery(CompositeQuery):
    """Match a field against a list of values."""
    def __init__(self, field, values):
        self.field = field
        self.values = values

    def to_tuple(self):
        return (self.field, "in") + tuple(self.values)


class ZipRadiusQuery(CompositeQuery):
    """Takes a single zip code which will be the center of the search"""
    def __init__(self, field, radius, zip):
        if radius not in [5, 10, 15, 20, 25, 50]:
            raise Exception("radius can be one of 5, 10, 15, 20, 25, or 50")
        self.field = field
        self.radius = radius
        self.zip = zip

    def to_tuple(self):
        return self.field, "zip-radius:%s" % self.radius, "%s" % self.zip
