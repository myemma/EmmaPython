from . import BaseApiModel, ModelWithDateFields


class Group(BaseApiModel, ModelWithDateFields):
    def __init__(self, account, raw=None):
        self.account = account
        super(Group, self).__init__(raw)

    def _parse_raw(self, raw):
        self._str_fields_to_datetime(['deleted_at'], raw)
        return raw
