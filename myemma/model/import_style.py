"""The audience import styles"""
class ImportStyle(object):
    """Abstract Factory for import styles"""
    _code = None

    @classmethod
    def get_code(cls):
        """The Emma API coded value"""
        return cls._code

    @staticmethod
    def factory(status_or_code):
        """Abstract factory"""
        return {
            AddOnly: AddOnly,
            AddOnly.get_code(): AddOnly,
            AddAndUpdate: AddAndUpdate,
            AddAndUpdate.get_code(): AddAndUpdate
        }[status_or_code]


class AddOnly(ImportStyle):
    """Import was to add members only"""
    _code = u"add_only"


class AddAndUpdate(ImportStyle):
    """Import was to add and/or update members"""
    _code = u"add_and_update"


