class MemberChangeType(object):
    _code = None

    @classmethod
    def get_code(cls):
        return cls._code

    @staticmethod
    def factory(status_or_code):
        return {
            Added: Added,
            Added.get_code(): Added,
            Confirmed: Confirmed,
            Confirmed.get_code(): Confirmed,
            Deleted: Deleted,
            Deleted.get_code(): Deleted,
            Undeleted: Undeleted,
            Undeleted.get_code(): Undeleted,
            Updated: Updated,
            Updated.get_code(): Updated,
            RejectedUpdate: RejectedUpdate,
            RejectedUpdate.get_code(): RejectedUpdate,
            SignedUp: SignedUp,
            SignedUp.get_code(): SignedUp,
            StatusShifted: StatusShifted,
            StatusShifted.get_code(): StatusShifted,
        }[status_or_code]


class Added(MemberChangeType):
    _code = u"a"


class Confirmed(MemberChangeType):
    _code = u"c"


class Deleted(MemberChangeType):
    _code = u"d"


class Undeleted(MemberChangeType):
    _code = u"n"


class Updated(MemberChangeType):
    _code = u"u"


class RejectedUpdate(MemberChangeType):
    _code = u"r"


class SignedUp(MemberChangeType):
    _code = u"s"


class StatusShifted(MemberChangeType):
    _code = u"t"
