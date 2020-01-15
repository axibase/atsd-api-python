from unittest import TestCase
from atsd_client.models import Horizon, TimeUnit, Interval

INTERVAL_COUNT = 1
INTERVAL_UNIT = TimeUnit.DAY
INTERVAL = Interval(INTERVAL_COUNT, INTERVAL_UNIT)
INTERVAL_DICT = {'count': INTERVAL_COUNT, 'unit': INTERVAL_UNIT}
LENGTH = 1
END_DATE = "next_day"
START_DATE = "current_day"

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestHorizon(TestCase):

    def test_init(self):
        horizon = Horizon(INTERVAL, LENGTH, END_DATE, START_DATE)
        self.assertEqual(INTERVAL, horizon.interval)
        self.assertEqual(LENGTH, horizon.length)
        self.assertEqual(END_DATE, horizon.endDate)
        self.assertEqual(START_DATE, horizon.startDate)

    def test_set_interval(self):
        horizon = Horizon()
        horizon.set_interval(count=INTERVAL_COUNT, unit=INTERVAL_UNIT)
        self.assertEqual(INTERVAL_DICT, horizon.interval)
        self.assertRaises(ValueError, horizon.set_interval, None, INCORRECT_VALUE, INTERVAL_UNIT)
        self.assertRaises(ValueError, horizon.set_interval, None, INTERVAL_COUNT, INCORRECT_VALUE)

    def test_set_interval_dict(self):
        horizon = Horizon()
        horizon.set_interval(INTERVAL)
        self.assertEqual(INTERVAL, horizon.interval)
        horizon.set_interval(INTERVAL_DICT)
        self.assertEqual(INTERVAL_DICT, horizon.interval)
        self.assertRaises(ValueError, horizon.set_interval, {'count': INTERVAL_COUNT,
                                                                  INCORRECT_VALUE: INTERVAL_UNIT})
        self.assertRaises(ValueError, horizon.set_interval, {'count': INCORRECT_VALUE, 'unit': INTERVAL_UNIT})
        self.assertRaises(ValueError, horizon.set_interval, {'count': INTERVAL_COUNT, 'unit': INCORRECT_VALUE})

    def test_set_length(self):
        horizon = Horizon()
        horizon.set_length(LENGTH)
        self.assertEqual(LENGTH, horizon.length)
        self.assertRaises(ValueError, horizon.set_length, INCORRECT_VALUE)

    def test_set_end_date(self):
        horizon = Horizon()
        horizon.set_end_date(END_DATE)
        self.assertEqual(END_DATE, horizon.endDate)
        self.assertRaises(ValueError, horizon.set_end_date, 1)

    def test_set_start_date(self):
        horizon = Horizon()
        horizon.set_start_date(START_DATE)
        self.assertEqual(START_DATE, horizon.startDate)
        self.assertRaises(ValueError, horizon.set_start_date, 1)
