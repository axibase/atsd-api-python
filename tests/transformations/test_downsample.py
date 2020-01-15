from unittest import TestCase
from atsd_client.models import Downsample, DownsampleAlgorithm, Interval, TimeUnit

ALGORITHM = DownsampleAlgorithm.DETAIL
DIFFERENCE = 1
RATIO = 1
GAP_COUNT = 1
GAP_UNIT = TimeUnit.DAY
GAP_INTERVAL = Interval(GAP_COUNT, GAP_UNIT)
GAP_DICT = {'count': GAP_COUNT, 'unit': GAP_UNIT}

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestDownsample(TestCase):

    def test_init(self):
        downsample = Downsample(ALGORITHM, DIFFERENCE, RATIO, GAP_INTERVAL)
        self.assertEqual(ALGORITHM, downsample.algorithm)
        self.assertEqual(DIFFERENCE, downsample.difference)
        self.assertEqual(RATIO, downsample.ratio)
        self.assertEqual(GAP_INTERVAL, downsample.gap)

    def test_set_algorithm(self):
        downsample = Downsample()
        downsample.set_algorithm(ALGORITHM)
        self.assertEqual(ALGORITHM, downsample.algorithm)
        self.assertRaises(ValueError, downsample.set_algorithm, INCORRECT_VALUE)

    def test_set_difference(self):
        downsample = Downsample()
        downsample.set_difference(DIFFERENCE)
        self.assertEqual(DIFFERENCE, downsample.difference)
        self.assertRaises(ValueError, downsample.set_difference, INCORRECT_VALUE)

    def test_set_ratio(self):
        downsample = Downsample()
        downsample.set_ratio(RATIO)
        self.assertEqual(RATIO, downsample.ratio)
        self.assertRaises(ValueError, downsample.set_ratio, INCORRECT_VALUE)

    def test_set_gap(self):
        downsample = Downsample()
        downsample.set_gap(count=GAP_COUNT, unit=GAP_UNIT)
        self.assertEqual(GAP_DICT, downsample.gap)
        self.assertRaises(ValueError, downsample.set_gap, INCORRECT_VALUE, GAP_UNIT)
        self.assertRaises(ValueError, downsample.set_gap, GAP_COUNT, INCORRECT_VALUE)

    def test_set_gap_dict(self):
        downsample = Downsample()
        downsample.set_gap(GAP_INTERVAL)
        self.assertEqual(GAP_INTERVAL, downsample.gap)
        downsample.set_gap(GAP_DICT)
        self.assertEqual(GAP_DICT, downsample.gap)
        self.assertRaises(ValueError, downsample.set_gap, {'count': GAP_COUNT, 'incorrect_param': GAP_UNIT})
        self.assertRaises(ValueError, downsample.set_gap, {'count': INCORRECT_VALUE, 'unit': GAP_UNIT})
        self.assertRaises(ValueError, downsample.set_gap, {'count': GAP_COUNT, 'unit': INCORRECT_VALUE})
