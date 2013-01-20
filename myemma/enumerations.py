"""Emma API Enumerations"""


class Enum(object):
    """Base class"""
    pass


class MemberStatus(Enum):
    """Member Status"""
    Active = "a"
    Error = "e"
    Forwarded = "f"
    OptOut = "o"


class DeliveryType(Enum):
    """Delivery Type"""
    Delivered = "d"
    HardBounce = "b"
    SoftBounce = "s"



class GroupType(Enum):
    """Group Type"""
    RegularGroup = "g"
    TestGroup = "t"
    HiddenGroup = "h"



class ImportStatus(Enum):
    """Import Status"""
    Ok = "o"
    Error = "e"


class ImportStyle(Enum):
    """Import Style"""
    AddOnly = "add_only"
    AddAndUpdate = "add_and_update"


class MemberChangeType(Enum):
    """Member Change Types"""
    Added = "a"
    Confirmed = "c"
    Deleted = "d"
    Undeleted = "n"
    Updated = "u"
    RejectedUpdate = "r"
    SignedUp = "s"
    StatusShifted = "t"


