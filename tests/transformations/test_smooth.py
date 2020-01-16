from unittest import TestCase

from atsd_client.models import Smooth, SmoothType, Interval, TimeUnit

TYPE = SmoothType.AVG
INTERVAL = Interval(1, TimeUnit.DAY)
DICT_INTERVAL = {'count': 1, 'unit': TimeUnit.DAY}
COUNT = 1
MINIMUM_COUNT = 1
INCOMPLETE_VALUE = "null"

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestSmooth(TestCase):

    def test_init(self):
        smooth = Smooth(TYPE, COUNT, INTERVAL, MINIMUM_COUNT, INCOMPLETE_VALUE)
        self.assertEqual(TYPE, smooth.type)
        self.assertEqual(COUNT, smooth.count)
        self.assertEqual(INTERVAL, smooth.interval)
        self.assertEqual(MINIMUM_COUNT, smooth.minimumCount)
        self.assertEqual(INCOMPLETE_VALUE, smooth.incompleteValue)

    def test_set_type(self):
        smooth = Smooth(TYPE)
        smooth.set_type(SmoothType.COUNT)
        self.assertEqual(SmoothType.COUNT, smooth.type)
        self.assertRaises(ValueError, smooth.set_type, INCORRECT_VALUE)

    def test_set_count(self):
        smooth = Smooth(TYPE)
        smooth.set_count(COUNT)
        self.assertEqual(COUNT, smooth.count)
        self.assertRaises(ValueError, smooth.set_count, INCORRECT_VALUE)

    def test_set_interval(self):
        smooth = Smooth(TYPE)
        smooth.set_interval(count=1, unit=TimeUnit.DAY)
        self.assertEqual(DICT_INTERVAL, smooth.interval)
        self.assertRaises(ValueError, smooth.set_interval, None, 1, INCORRECT_VALUE)
        self.assertRaises(ValueError, smooth.set_interval, None, INCORRECT_VALUE, TimeUnit.DAY)

    def test_set_interval_dict(self):
        smooth = Smooth(TYPE)
        smooth.set_interval(INTERVAL)
        self.assertEqual(INTERVAL, smooth.interval)
        smooth.set_interval(DICT_INTERVAL)
        self.assertEqual(DICT_INTERVAL, smooth.interval)
        self.assertRaises(ValueError, smooth.set_interval, {'count': 1, 'incorrect_param': TimeUnit.DAY})
        self.assertRaises(ValueError, smooth.set_interval, {'count': INCORRECT_VALUE, 'unit': TimeUnit.DAY})
        self.assertRaises(ValueError, smooth.set_interval, {'count': 1, 'unit': INCORRECT_VALUE})

    def test_set_minimum_count(self):
        smooth = Smooth(TYPE)
        smooth.set_minimum_count(MINIMUM_COUNT)
        self.assertEqual(MINIMUM_COUNT, smooth.minimumCount)
        self.assertRaises(ValueError, smooth.set_minimum_count, INCORRECT_VALUE)

    def test_set_incomplete_value(self):
        smooth = Smooth(TYPE)
        smooth.set_incomplete_value(INCOMPLETE_VALUE)
        self.assertEqual(INCOMPLETE_VALUE, smooth.incompleteValue)
        self.assertRaises(ValueError, smooth.set_incomplete_value, 1)
