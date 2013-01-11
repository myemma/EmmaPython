from base import BaseApiModel

class Collection(BaseApiModel):
    def __init__(self, adapter):
        self.adapter = adapter
        self._dict = {}

    def replace_all(self, items):
        for id in items.keys():
            self._dict[id] = items[id]

__all__ = ['Collection']
