from . import BaseApiModel, ModelWithDateFields
import group_type


class Group(BaseApiModel, ModelWithDateFields):
    def __init__(self, account, raw=None):
        self.account = account
        super(Group, self).__init__(raw)

    def _parse_raw(self, raw):
        if 'group_type' in raw:
            raw['group_type'] = group_type.GroupType.factory(raw['group_type'])
        self._str_fields_to_datetime(['deleted_at'], raw)
        return raw
