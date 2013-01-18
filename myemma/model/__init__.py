import collections
import datetime


SERIALIZED_DATETIME_FORMAT = "@D:%Y-%m-%dT%H:%M:%S"


class NoMemberEmailError(Exception):
    """
    An API call was attempted with missing required parameters (email)
    """
    pass


class NoMemberIdError(Exception):
    """
    An API call was attempted with missing required parameters (id)
    """
    pass


class NoMemberStatusError(Exception):
    """
    An API call was attempted with missing required parameters (status)
    """
    pass


class MemberDeleteError(Exception):
    """
    The API call to delete a member did not complete correctly
    """
    pass


class MemberChangeStatusError(Exception):
    """
    The API call to change a member's status did not complete correctly
    """
    pass


class MemberUpdateError(Exception):
    """
    The API call to update a member's information did not complete correctly
    """
    pass


class MemberDropGroupError(Exception):
    """
    The API call to drop groups from a member did not complete correctly
    """
    pass


class BaseApiModel(collections.MutableMapping):
    def __init__(self, raw=None):
        self._dict = self._parse_raw(raw) if raw else {}

    def __len__(self):
        return self._dict.__len__()

    def __getitem__(self, key):
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

    def _replace_all(self, items):
        is_new = lambda x: x[0] not in self._dict
        replace = lambda x: (x[0], x[1] if x[0] not in items else items[x[0]])

        if not self._dict:
            self._dict = items
        else:
            self._dict = dict(
                map(replace, self._dict.items())
                + filter(is_new, items.items())
            )

    def _parse_raw(self, raw):
        return raw

class ModelWithDateFields(object):
    def _str_fields_to_datetime(self, fields, raw):
        for field in fields:
            if field in raw and raw[field]:
                raw[field] = datetime.datetime.strptime(
                    raw[field],
                    SERIALIZED_DATETIME_FORMAT)