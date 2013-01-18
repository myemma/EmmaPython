"""The audience member change types"""
class MemberChangeType(object):
    """Abstract Factory for member change types"""
    _code = None

    @classmethod
    def get_code(cls):
        """The Emma API coded value"""
        return cls._code

    @staticmethod
    def factory(status_or_code):
        """Abstract factory"""
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
    """Member was added"""
    _code = u"a"


class Confirmed(MemberChangeType):
    """Member was confirmed"""
    _code = u"c"


class Deleted(MemberChangeType):
    """Member was deleted"""
    _code = u"d"


class Undeleted(MemberChangeType):
    """Member was undeleted"""
    _code = u"n"


class Updated(MemberChangeType):
    """Member was updated"""
    _code = u"u"


class RejectedUpdate(MemberChangeType):
    """Member update was rejected"""
    _code = u"r"


class SignedUp(MemberChangeType):
    """Member was signed-up"""
    _code = u"s"


class StatusShifted(MemberChangeType):
    """Member's status was changed"""
    _code = u"t"
