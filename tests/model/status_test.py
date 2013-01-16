import unittest
from myemma.model.status import (Active, Error, Forwarded, OptOut)


class StatusTest(unittest.TestCase):
    def test_active_status_returns_correct_code_and_name(self):
        self.assertEquals(u"a", Active.get_code())
        self.assertEquals(u"active", Active.get_name())

    def test_error_status_returns_correct_code_and_name(self):
        self.assertEquals(u"e", Error.get_code())
        self.assertEquals(u"error", Error.get_name())

    def test_forwarded_status_returns_correct_code_and_name(self):
        self.assertEquals(u"f", Forwarded.get_code())
        self.assertEquals(u"forwarded", Forwarded.get_name())

    def test_optout_status_returns_correct_code_and_name(self):
        self.assertEquals(u"o", OptOut.get_code())
        self.assertEquals(u"opt-out", OptOut.get_name())