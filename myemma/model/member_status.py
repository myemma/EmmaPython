"""The audience member statuses"""
class MemberStatus(object):
    """Abstract Factory for member statuses"""
    _code = None
    _name = None

    @classmethod
    def get_code(cls):
        """The Emma API coded value"""
        return cls._code

    @classmethod
    def get_name(cls):
        """The Emma API name"""
        return cls._name

    @staticmethod
    def factory(status_or_name_or_code):
        """Abstract factory"""
        return {
            Active: Active,
            Active.get_code(): Active,
            Active.get_name(): Active,
            Error: Error,
            Error.get_code(): Error,
            Error.get_name(): Error,
            Forwarded: Forwarded,
            Forwarded.get_code(): Forwarded,
            Forwarded.get_name(): Forwarded,
            OptOut: OptOut,
            OptOut.get_code(): OptOut,
            OptOut.get_name(): OptOut
        }[status_or_name_or_code]


class Active(MemberStatus):
    """Member is active"""
    _code = u"a"
    _name = u"active"


class Error(MemberStatus):
    """Member has an error"""
    _code = u"e"
    _name = u"error"


class Forwarded(MemberStatus):
    """Member was forwarded"""
    _code = u"f"
    _name = u"forwarded"

class OptOut(MemberStatus):
    """Member is opted-out"""
    _code = u"o"
    _name = u"opt-out"
