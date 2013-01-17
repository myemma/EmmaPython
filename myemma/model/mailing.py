from . import BaseApiModel, ModelWithDateFields
from delivery_type import DeliveryType


class Mailing(BaseApiModel, ModelWithDateFields):
    def __init__(self, account, raw = None):
        self.account = account
        self._dict = self._parse_raw(raw) if raw is not None else {}

    def _parse_raw(self, raw):
        if 'delivery_type' in raw:
            raw['delivery_type'] = DeliveryType.factory(raw['delivery_type'])
        self._str_fields_to_datetime(
            ['clicked', 'opened', 'delivery_ts', 'forwarded', 'shared', 'sent'],
            raw)
        return raw
