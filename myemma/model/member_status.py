class MemberStatus(object):
    _code = None
    _name = None

    @classmethod
    def get_code(cls):
        return cls._code

    @classmethod
    def get_name(cls):
        return cls._name

    @staticmethod
    def factory(status_or_name_or_code):
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
    _code = u"a"
    _name = u"active"


class Error(MemberStatus):
    _code = u"e"
    _name = u"error"


class Forwarded(MemberStatus):
    _code = u"f"
    _name = u"forwarded"

class OptOut(MemberStatus):
    _code = u"o"
    _name = u"opt-out"
