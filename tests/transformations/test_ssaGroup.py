from unittest import TestCase
from atsd_client.models import SsaGroup, SsaGroupAuto, SsaGroupManual

GROUP_AUTO = SsaGroupAuto()
GROUP_MANUAL = SsaGroupManual()

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestSsaGroup(TestCase):

    def test_init(self):
        group = SsaGroup(GROUP_AUTO, GROUP_MANUAL)
        self.assertEqual(GROUP_AUTO, group.auto)
        self.assertEqual(GROUP_MANUAL, group.manual)

    def test_set_auto(self):
        group = SsaGroup()
        group.set_auto(GROUP_AUTO)
        self.assertEqual(GROUP_AUTO, group.auto)
        self.assertRaises(ValueError, group.set_auto, INCORRECT_VALUE)

    def test_set_manual(self):
        group = SsaGroup()
        group.set_manual(GROUP_MANUAL)
        self.assertEqual(GROUP_MANUAL, group.manual)
        self.assertRaises(ValueError, group.set_manual, INCORRECT_VALUE)
