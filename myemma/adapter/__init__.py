"""
Provides a place to put any layer of abstraction between this wrapper and a
needed HTTP client library
"""

class ApiRequestFailed(Exception):
    """
    Denotes a failure interacting with the API, such as HTTP 401 Unauthorized
    """
    pass


class ImportDeleteError(Exception):
    """
    The API call to mark an import as deleted did not complete correctly
    """
    pass


class MemberChangeStatusError(Exception):
    """
    The API call to change a member's status did not complete correctly
    """
    pass


class MemberCopyToGroupError(Exception):
    """
    The API call to copy members into a group did not complete correctly
    """
    pass


class MemberDeleteError(Exception):
    """
    The API call to delete a member did not complete correctly
    """
    pass


class MemberDropGroupError(Exception):
    """
    The API call to drop groups from a member did not complete correctly
    """
    pass


class MemberUpdateError(Exception):
    """
    The API call to update a member's information did not complete correctly
    """
    pass


class NoMemberEmailError(Exception):
    """
    An API call was attempted with missing required parameters (email)
    """
    pass


class NoMemberIdError(Exception):
    """
    An API call was attempted with missing required parameters (member_id)
    """
    pass


class NoMemberStatusError(Exception):
    """
    An API call was attempted with missing required parameters (status)
    """
    pass


class NoGroupIdError(Exception):
    """
    An API call was attempted with missing required parameters (member_group_id)
    """
    pass


class NoImportIdError(Exception):
    """
    An API call was attempted with missing required parameters (import_id)
    """
    pass


class NoFieldIdError(Exception):
    """
    An API call was attempted with missing required parameters (field_id)
    """
    pass


class AbstractAdapter(object):
    """
    Abstract Adapter
    """
    def post(self, path, params=None):
        """HTTP POST"""
        pass

    def get(self, path, params=None):
        """HTTP GET"""
        pass

    def put(self, path, params=None):
        """HTTP PUT"""
        pass

    def delete(self, path, params=None):
        """HTTP DELETE"""
        pass
