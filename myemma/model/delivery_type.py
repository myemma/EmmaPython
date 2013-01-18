class DeliveryType(object):
    _code = None

    @classmethod
    def get_code(cls):
        return cls._code

    @staticmethod
    def factory(status_or_code):
        return {
            Delivered: Delivered,
            Delivered.get_code(): Delivered,
            HardBounce: HardBounce,
            HardBounce.get_code(): HardBounce,
            SoftBounce: SoftBounce,
            SoftBounce.get_code(): SoftBounce
        }[status_or_code]


class Delivered(DeliveryType):
    _code = u"d"


class HardBounce(DeliveryType):
    _code = u"b"


class SoftBounce(DeliveryType):
    _code = u"s"


