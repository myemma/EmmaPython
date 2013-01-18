"""The mailing delivery types"""
class DeliveryType(object):
    """Abstract Factory for delivery types"""
    _code = None

    @classmethod
    def get_code(cls):
        """The Emma API coded value"""
        return cls._code

    @staticmethod
    def factory(status_or_code):
        """Abstract factory"""
        return {
            Delivered: Delivered,
            Delivered.get_code(): Delivered,
            HardBounce: HardBounce,
            HardBounce.get_code(): HardBounce,
            SoftBounce: SoftBounce,
            SoftBounce.get_code(): SoftBounce
        }[status_or_code]


class Delivered(DeliveryType):
    """Mailing was delivered"""
    _code = u"d"


class HardBounce(DeliveryType):
    """Mailing hard bounced"""
    _code = u"b"


class SoftBounce(DeliveryType):
    """Mailing soft bounced"""
    _code = u"s"


