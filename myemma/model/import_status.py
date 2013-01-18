"""The audience import statuses"""
class ImportStatus(object):
    """Abstract Factory for import statuses"""
    _code = None

    @classmethod
    def get_code(cls):
        """The Emma API coded value"""
        return cls._code

    @staticmethod
    def factory(status_or_code):
        """Abstract factory"""
        return {
            Ok: Ok,
            Ok.get_code(): Ok,
            Error: Error,
            Error.get_code(): Error
        }[status_or_code]


class Ok(ImportStatus):
    """Import completed successfully"""
    _code = u"o"


class Error(ImportStatus):
    """There was an error in the import"""
    _code = u"e"


