class ImportStyle(object):
    @classmethod
    def get_code(cls):
        return cls._code

    @staticmethod
    def factory(status_or_code):
        return {
            AddOnly: AddOnly,
            AddOnly._code: AddOnly,
            AddAndUpdate: AddAndUpdate,
            AddAndUpdate._code: AddAndUpdate
        }[status_or_code]


class AddOnly(ImportStyle):
    _code = u"add_only"


class AddAndUpdate(ImportStyle):
    _code = u"add_and_update"


