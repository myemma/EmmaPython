from . import BaseApiModel


class Group(BaseApiModel):
    def __init__(self, account, raw = None):
        self.account = account
        self._dict = raw if raw is not None else {}
