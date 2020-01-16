from unittest import TestCase
from atsd_client.models import SsaGroupManual

GROUPS = ['group']

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestSsaGroupManual(TestCase):

    def test_init(self):
        manual = SsaGroupManual(GROUPS)
        self.assertEqual(GROUPS, manual.groups)

    def test_set_groups(self):
        manual = SsaGroupManual()
        manual.set_groups(GROUPS)
        self.assertEqual(GROUPS, manual.groups)
        self.assertRaises(ValueError, manual.set_groups, INCORRECT_VALUE)
