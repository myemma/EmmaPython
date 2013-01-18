from . import BaseApiModel


class Field(BaseApiModel):
    def __init__(self, account, raw=None):
        self.account = account
        super(Field, self).__init__(raw)

