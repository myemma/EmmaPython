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


class WebHookMethod(Enum):
    """WebHook Method"""
    GET = "GET"
    POST = "POST"


class EventType(Enum):
    """Event Type"""
    SignUp = "s"
    Click = "c"
    Survey = "u"
    Date = "d"
    RecurringDate = "r"


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


class FieldType(Enum):
    """Field Type"""
    Text = "text"
    TextArray = "text[]"
    Numeric = "numeric"
    Boolean = "boolean"
    Date = "date"
    Timestamp = "timestamp"


class WidgetType(Enum):
    """Widget Type"""
    ShortAnswer = "text"
    LongAnswer = "long"
    CheckBoxMenu = "checkbox"
    SelectMultiple = "select multiple"
    CheckMultiple = "check_multiple"
    RadioButtonMenu = "radio"
    DatePicker = "date"
    DropDownMenu = "select one"
    Number = "number"


class MailingType(Enum):
    """Mailing Types"""
    Standard = "m"
    Test = "t"
    Trigger = "r"


class MailingStatus(Enum):
    """Mailing Status"""
    Pending = "p"
    Ready = "p"
    Paused = "a"
    Sending = "s"
    Canceled = "x"
    Complete = "c"
    Failed = "f"


class PersonalizedMessageType(Enum):
    """Personalized Message Types"""
    Html = "html"
    PlainText = "plaintext"
    Subject = "subject"


class Report(Enum):
    """Report Types"""
    ResponseSummary = 0
    MailingSummary = 1
    SentList = 2
    InProgressList = 3
    DeliveredList = 4
    OpenList = 5
    LinkList = 6
    ClickList = 7
    ForwardList = 8
    OptOutList = 9
    SignUpList = 10
    SharesList = 11
    CustomerSharesList = 12
    CustomerShareClicksList = 13
    CustomerShare = 14
    SharesOverview = 15
