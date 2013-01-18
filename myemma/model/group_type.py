"""The audience group types"""
class GroupType(object):
    """Abstract Factory for group types"""
    _code = None

    @classmethod
    def get_code(cls):
        """The Emma API coded value"""
        return cls._code

    @staticmethod
    def factory(status_or_code):
        """Abstract factory"""
        return {
            RegularGroup: RegularGroup,
            RegularGroup.get_code(): RegularGroup,
            TestGroup: TestGroup,
            TestGroup.get_code(): TestGroup,
            HiddenGroup: HiddenGroup,
            HiddenGroup.get_code(): HiddenGroup
        }[status_or_code]


class RegularGroup(GroupType):
    """A regular group"""
    _code = u"g"


class TestGroup(GroupType):
    """A test group"""
    _code = u"t"


class HiddenGroup(GroupType):
    """A hidden group"""
    _code = u"h"
