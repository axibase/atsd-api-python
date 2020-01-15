from unittest import TestCase
from atsd_client.models import HoltWinters, TimeUnit, Interval

AUTO = True
PERIOD_COUNT = 1
PERIOD_UNIT = TimeUnit.DAY
PERIOD_INTERVAL = Interval(PERIOD_COUNT, PERIOD_UNIT)
PERIOD_DICT = {'count': PERIOD_COUNT, 'unit': PERIOD_UNIT}
ALPHA = 1
BETA = 1
GAMMA = 1

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestHoltWinters(TestCase):

    def test_init(self):
        hw = HoltWinters(AUTO, PERIOD_INTERVAL, ALPHA, BETA, GAMMA)
        self.assertEqual(AUTO, hw.auto)
        self.assertEqual(PERIOD_INTERVAL, hw.period)
        self.assertEqual(ALPHA, hw.alpha)
        self.assertEqual(BETA, hw.beta)
        self.assertEqual(GAMMA, hw.gamma)

    def test_set_auto(self):
        hw = HoltWinters()
        hw.set_auto(AUTO)
        self.assertEqual(AUTO, hw.auto)
        self.assertRaises(ValueError, hw.set_auto, INCORRECT_VALUE)

    def test_set_period(self):
        hw = HoltWinters()
        hw.set_period(count=PERIOD_COUNT, unit=PERIOD_UNIT)
        self.assertEqual(PERIOD_DICT, hw.period)
        self.assertRaises(ValueError, hw.set_period, None, INCORRECT_VALUE, PERIOD_UNIT)
        self.assertRaises(ValueError, hw.set_period, None, PERIOD_COUNT, INCORRECT_VALUE)

    def test_set_period_dict(self):
        hw = HoltWinters()
        hw.set_period(PERIOD_INTERVAL)
        self.assertEqual(PERIOD_INTERVAL, hw.period)
        hw.set_period(PERIOD_DICT)
        self.assertEqual(PERIOD_DICT, hw.period)
        self.assertRaises(ValueError, hw.set_period, {'count': PERIOD_COUNT, 'incorrect_param': PERIOD_UNIT})
        self.assertRaises(ValueError, hw.set_period, {'count': INCORRECT_VALUE, 'unit': PERIOD_UNIT})
        self.assertRaises(ValueError, hw.set_period, {'count': PERIOD_COUNT, 'unit': INCORRECT_VALUE})

    def test_set_alpha(self):
        hw = HoltWinters()
        hw.set_alpha(ALPHA)
        self.assertEqual(ALPHA, hw.alpha)
        self.assertRaises(ValueError, hw.set_alpha, INCORRECT_VALUE)

    def test_set_beta(self):
        hw = HoltWinters()
        hw.set_beta(BETA)
        self.assertEqual(BETA, hw.beta)
        self.assertRaises(ValueError, hw.set_beta, INCORRECT_VALUE)

    def test_set_gamma(self):
        hw = HoltWinters()
        hw.set_gamma(GAMMA)
        self.assertEqual(GAMMA, hw.gamma)
        self.assertRaises(ValueError, hw.set_gamma, INCORRECT_VALUE)
