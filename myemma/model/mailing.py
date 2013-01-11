from base import BaseApiModel

class Mailing(BaseApiModel):

    def __init__(self, adapter, raw = None):
        self.adapter = adapter
        self._dict = raw if raw is not None else {}

__all__ = ['Mailing']