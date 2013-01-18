class ImportStatus(object):
    _code = None

    @classmethod
    def get_code(cls):
        return cls._code

    @staticmethod
    def factory(status_or_code):
        return {
            Ok: Ok,
            Ok.get_code(): Ok,
            Error: Error,
            Error.get_code(): Error
        }[status_or_code]


class Ok(ImportStatus):
    _code = u"o"


class Error(ImportStatus):
    _code = u"e"


