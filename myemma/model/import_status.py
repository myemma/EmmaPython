class ImportStatus(object):
    @staticmethod
    def factory(status_or_code):
        return {
            Ok: Ok,
            u"o": Ok,
            Error: Error,
            u"e": Error
        }[status_or_code]


class Ok(ImportStatus): pass
class Error(ImportStatus): pass
