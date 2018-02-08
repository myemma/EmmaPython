from datetime import datetime
import unittest

from emma.model import SERIALIZED_DATETIME_ALT_FORMAT
from emma import exceptions as ex
from emma.model.account import Account
from emma.model.automation import Workflow

from tests.model import MockAdapter


class WorkflowTest(unittest.TestCase):
    """
    Tests for the Workflow model
    """

    def setUp(self):
        """
        Set up tasks for our tests
        """
        Account.default_adapter = MockAdapter
        self.workflow = Workflow(
            Account(account_id="100", public_key="xxx", private_key="yyy"),
            {
                'workflow_id': '22048a49-9533-4014-ae03-2af3598ed9a7',
                'status': 'active',
                'name': 'Test',
                'created_at': datetime.now().strftime(SERIALIZED_DATETIME_ALT_FORMAT),
                'updated_at': datetime.now().strftime(SERIALIZED_DATETIME_ALT_FORMAT),
            }
        )

    def test_can_represent_workflow(self):
        self.assertEquals(
            u"<Workflow" + repr(self.workflow._dict) + u">",
            repr(self.workflow))
