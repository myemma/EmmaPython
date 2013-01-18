class ImportStyle(object):
    _code = None

    @classmethod
    def get_code(cls):
        return cls._code

    @staticmethod
    def factory(status_or_code):
        return {
            AddOnly: AddOnly,
            AddOnly.get_code(): AddOnly,
            AddAndUpdate: AddAndUpdate,
            AddAndUpdate.get_code(): AddAndUpdate
        }[status_or_code]


class AddOnly(ImportStyle):
    _code = u"add_only"


class AddAndUpdate(ImportStyle):
    _code = u"add_and_update"


