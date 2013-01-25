"""You need models. We got models."""

import collections
from datetime import datetime


SERIALIZED_DATETIME_FORMAT = "@D:%Y-%m-%dT%H:%M:%S"


def str_fields_to_datetime(fields, raw):
    """Parses Emma date fields to :class:`datetime` objects"""
    return dict((x[0], datetime.strptime(x[1], SERIALIZED_DATETIME_FORMAT))
        for x in raw.items() if x[0] in fields and x[1] is not None)


class BaseApiModel(collections.MutableMapping):
    """Creates a model with dictionary access"""
    def __init__(self, raw=None):
        self._dict = self._parse_raw(raw) if raw else {}

    def __len__(self):
        return self._dict.__len__()

    def __getitem__(self, key):
        if key not in self._dict:
            raise KeyError(key)
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        self._dict.__setitem__(key, value)

    def __delitem__(self, key):
        self._dict.__delitem__(key)

    def __iter__(self):
        return self._dict.__iter__()

    def __contains__(self, key):
        return self._dict.__contains__(key)

    def __repr__(self):
        return "".join(['<', self.__class__.__name__, repr(self._dict), '>'])

    def clear(self):
        self._dict = {}

    def _replace_all(self, items):
        """Update the internal :class:`dict` with matching items provided"""
        is_new = lambda x: x[0] not in self._dict
        replace = lambda x: (x[0], x[1] if x[0] not in items else items[x[0]])

        if not self._dict:
            self._dict = items
        else:
            self._dict = dict(
                [replace(x) for x in self._dict.items()]
                + [x for x in items.items() if is_new(x)]
            )

    def _parse_raw(self, raw):
        """
        Placeholder, will normally be overridden

        :param raw: The raw API value to parse
        :type raw: :class:`dict`
        """
        return raw

class BaseAPIEnum(object):
    """Abstract Factory for an enumeration"""
    _code = None

    @classmethod
    def get_code(cls):
        """The Emma API coded value"""
        return cls._code