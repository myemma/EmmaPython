"""Wrapper Exceptions"""

class ApiRequestFailed(Exception):
    """
    Denotes a failure interacting with the API, such as HTTP 401 Unauthorized
    """
    pass


class ImportDeleteError(ApiRequestFailed):
    """
    The API call to mark an import as deleted did not complete correctly
    """
    pass


class MemberChangeStatusError(ApiRequestFailed):
    """
    The API call to change a member's status did not complete correctly
    """
    pass


class MemberCopyToGroupError(ApiRequestFailed):
    """
    The API call to copy members into a group did not complete correctly
    """
    pass


class MemberDeleteError(ApiRequestFailed):
    """
    The API call to delete a member did not complete correctly
    """
    pass


class MemberDropGroupError(ApiRequestFailed):
    """
    The API call to drop groups from a member did not complete correctly
    """
    pass


class MemberUpdateError(ApiRequestFailed):
    """
    The API call to update a member's information did not complete correctly
    """
    pass


class NoMemberEmailError(ApiRequestFailed):
    """
    An API call was attempted with missing required parameters (email)
    """
    pass


class NoMemberIdError(ApiRequestFailed):
    """
    An API call was attempted with missing required parameters (member_id)
    """
    pass


class NoMemberStatusError(ApiRequestFailed):
    """
    An API call was attempted with missing required parameters (status)
    """
    pass


class NoGroupIdError(ApiRequestFailed):
    """
    An API call was attempted with missing required parameters (member_group_id)
    """
    pass


class NoImportIdError(ApiRequestFailed):
    """
    An API call was attempted with missing required parameters (import_id)
    """
    pass


class NoFieldIdError(ApiRequestFailed):
    """
    An API call was attempted with missing required parameters (field_id)
    """
    pass


class ClearMemberFieldInformationError(ApiRequestFailed):
    """
    An API call to clear member info from a field did not complete correctly
    """
    pass