class DeliveryType(object):
    @staticmethod
    def factory(status_or_code):
        return {
            Delivered: Delivered,
            u"d": Delivered,
            HardBounce: HardBounce,
            u"b": HardBounce,
            SoftBounce: SoftBounce,
            u"s": SoftBounce
        }[status_or_code]


class Delivered(DeliveryType): pass
class HardBounce(DeliveryType): pass
class SoftBounce(DeliveryType): pass
