from unittest import TestCase
from atsd_client.models import Baseline, TimeUnit, Interval, StatisticalFunction

PERIOD_COUNT = 1
PERIOD_UNIT = TimeUnit.DAY
PERIOD_INTERVAL = Interval(PERIOD_COUNT, PERIOD_UNIT)
PERIOD_DICT = {'count': PERIOD_COUNT, 'unit': PERIOD_UNIT}
COUNT = 1
FUNCTION = StatisticalFunction.COUNT
PERCENTILE = "PERCENTILE(90)"

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestBaseline(TestCase):

    def test_init(self):
        baseline = Baseline(PERIOD_INTERVAL, COUNT, FUNCTION)
        self.assertEqual(PERIOD_INTERVAL, baseline.period)
        self.assertEqual(COUNT, baseline.count)
        self.assertEqual(FUNCTION, baseline.function)

    def test_set_period(self):
        baseline = Baseline()
        baseline.set_period(count=PERIOD_COUNT, unit=PERIOD_UNIT)
        self.assertEqual(PERIOD_DICT, baseline.period)
        self.assertRaises(ValueError, baseline.set_period, INCORRECT_VALUE, PERIOD_UNIT)
        self.assertRaises(ValueError, baseline.set_period, PERIOD_COUNT, INCORRECT_VALUE)

    def test_set_period_dict(self):
        baseline = Baseline()
        baseline.set_period(PERIOD_INTERVAL)
        self.assertEqual(PERIOD_INTERVAL, baseline.period)
        baseline.set_period(PERIOD_DICT)
        self.assertEqual(PERIOD_DICT, baseline.period)
        self.assertRaises(ValueError, baseline.set_period, {'count': PERIOD_COUNT, INCORRECT_VALUE: PERIOD_UNIT})
        self.assertRaises(ValueError, baseline.set_period, {'count': INCORRECT_VALUE, 'unit': PERIOD_UNIT})
        self.assertRaises(ValueError, baseline.set_period, {'count': PERIOD_COUNT, 'unit': INCORRECT_VALUE})

    def test_set_count(self):
        baseline = Baseline()
        baseline.set_count(COUNT)
        self.assertEqual(COUNT, baseline.count)
        self.assertRaises(ValueError, baseline.set_count, INCORRECT_VALUE)

    def test_set_function(self):
        baseline = Baseline()
        baseline.set_function(FUNCTION)
        self.assertEqual(FUNCTION, baseline.function)
        baseline.set_function(PERCENTILE)
        self.assertEqual(PERCENTILE, baseline.function)
        self.assertRaises(ValueError, baseline.set_function, INCORRECT_VALUE)
