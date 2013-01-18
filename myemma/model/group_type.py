class GroupType(object):
    _code = None

    @classmethod
    def get_code(cls):
        return cls._code

    @staticmethod
    def factory(status_or_code):
        return {
            RegularGroup: RegularGroup,
            RegularGroup.get_code(): RegularGroup,
            TestGroup: TestGroup,
            TestGroup.get_code(): TestGroup,
            HiddenGroup: HiddenGroup,
            HiddenGroup.get_code(): HiddenGroup
        }[status_or_code]


class RegularGroup(GroupType):
    _code = u"g"


class TestGroup(GroupType):
    _code = u"t"


class HiddenGroup(GroupType):
    _code = u"h"
