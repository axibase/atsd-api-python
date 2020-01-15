from unittest import TestCase
from atsd_client.models import Interval, TimeUnit, Baseline
from atsd_client._jsonutil import serialize

COUNT = 1
UNIT = TimeUnit.DAY
EXPECTED = {"period": {"count": COUNT, "unit": UNIT}}


class IntervalTest(TestCase):

    def test_interval_obj(self):
        baseline = Baseline(period=Interval(COUNT, UNIT))
        self.assertEqual(EXPECTED, serialize(baseline))

    def test_interval_dict(self):
        baseline = Baseline(period={"count": COUNT, "unit": UNIT})
        self.assertEqual(EXPECTED, serialize(baseline))

    def test_intervalcount_and_unit(self):
        baseline = Baseline()
        baseline.set_period(count=COUNT, unit=UNIT)
        self.assertEqual(EXPECTED, serialize(baseline))
