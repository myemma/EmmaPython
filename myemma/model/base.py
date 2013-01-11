import collections

class ImmutableKeyError(Exception): pass

class BaseApiModel(collections.MutableMapping):
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
        return repr(self._dict)
