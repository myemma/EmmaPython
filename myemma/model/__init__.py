import collections


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


class Collection(BaseApiModel):
    """
    An object representing a set of models, useful for group-level operations

    :param adapter: An HTTP client adapter from :mod:`myemma.adapter`
    :type adapter: :class:`AbstractAdapter`
    """
    def __init__(self, adapter):
        self.adapter = adapter
        self._dict = {}

    def replace_all(self, items):
        """
        Update internal dictionary with newer items

        :param items: Dictionary of items to use as replacements
        :type items: :class:`dict`
        :rtype: :class:`None`

        """
        if not self._dict:
            self._dict = items
        else:
            self._dict = dict(
                map(
                    lambda x: (
                        x[0],
                        x[1] if x[0] not in items.keys() else items[x[0]]),
                    self._dict.items()
                ) + filter(
                    lambda x: x[0] not in self._dict.keys(),
                    items.items()
                )
            )