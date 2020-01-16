from unittest import TestCase
from atsd_client.models import ForecastTransformation, StatisticalFunction, TimeUnit, Interval, HoltWinters, Ssa, Arima, \
    Horizon, Baseline

AUTO_AGGREGATE = True
AGGREGATION_FUNCTION = StatisticalFunction.COUNT
PERCENTILE = "PERCENTILE(95)"
INCLUDE = ["include"]
SCORE_INTERVAL_COUNT = 1
SCORE_INTERVAL_UNIT = TimeUnit.DAY
SCORE_INTERVAL = Interval(SCORE_INTERVAL_COUNT, SCORE_INTERVAL_UNIT)
SCORE_INTERVAL_DICT = {'count': SCORE_INTERVAL_COUNT, 'unit': SCORE_INTERVAL_UNIT}
MIN_RANGE = 1
MAX_RANGE = 2
HOLTWINTERS = HoltWinters()
ARIMA = Arima()
SSA = Ssa()
HORIZON = Horizon()
BASELINE = Baseline()

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestForecastTransformation(TestCase):

    def test_init(self):
        forecast = ForecastTransformation(AUTO_AGGREGATE, AGGREGATION_FUNCTION, INCLUDE, SCORE_INTERVAL, MIN_RANGE,
                                          MAX_RANGE, HOLTWINTERS, ARIMA, SSA, HORIZON, BASELINE)
        self.assertEqual(AUTO_AGGREGATE, forecast.autoAggregate)
        self.assertEqual(AGGREGATION_FUNCTION, forecast.aggregationFunction)
        self.assertEqual(INCLUDE, forecast.include)
        self.assertEqual(SCORE_INTERVAL, forecast.scoreInterval)
        self.assertEqual({'min': MIN_RANGE, 'max': MAX_RANGE}, forecast.range)
        self.assertEqual(HOLTWINTERS, forecast.hw)
        self.assertEqual(ARIMA, forecast.arima)
        self.assertEqual(SSA, forecast.ssa)
        self.assertEqual(HORIZON, forecast.horizon)
        self.assertEqual(BASELINE, forecast.baseline)

    def test_set_auto_aggregate(self):
        forecast = ForecastTransformation()
        forecast.set_auto_aggregate(AUTO_AGGREGATE)
        self.assertEqual(AUTO_AGGREGATE, forecast.autoAggregate)
        self.assertRaises(ValueError, forecast.set_auto_aggregate, INCORRECT_VALUE)

    def test_set_aggregation_function(self):
        forecast = ForecastTransformation()
        forecast.set_aggregation_function(AGGREGATION_FUNCTION)
        self.assertEqual(AGGREGATION_FUNCTION, forecast.aggregationFunction)
        forecast.set_aggregation_function(PERCENTILE)
        self.assertEqual(PERCENTILE, forecast.aggregationFunction)
        self.assertRaises(ValueError, forecast.set_aggregation_function, INCORRECT_VALUE)

    def test_set_include(self):
        forecast = ForecastTransformation()
        forecast.set_include(INCLUDE)
        self.assertEqual(INCLUDE, forecast.include)

    def test_set_score_interval(self):
        forecast = ForecastTransformation()
        forecast.set_score_interval(count=SCORE_INTERVAL_COUNT, unit=SCORE_INTERVAL_UNIT)
        self.assertEqual(SCORE_INTERVAL_DICT, forecast.scoreInterval)
        self.assertRaises(ValueError, forecast.set_score_interval, None, INCORRECT_VALUE, SCORE_INTERVAL_UNIT)
        self.assertRaises(ValueError, forecast.set_score_interval, None, SCORE_INTERVAL_COUNT, INCORRECT_VALUE)

    def test_set_score_interval_dict(self):
        forecast = ForecastTransformation()
        forecast.set_score_interval(SCORE_INTERVAL)
        self.assertEqual(SCORE_INTERVAL, forecast.scoreInterval)
        forecast.set_score_interval(SCORE_INTERVAL_DICT)
        self.assertEqual(SCORE_INTERVAL_DICT, forecast.scoreInterval)
        self.assertRaises(ValueError, forecast.set_score_interval, {'count': SCORE_INTERVAL_COUNT,
                                                                         'incorrect_param': SCORE_INTERVAL_UNIT})
        self.assertRaises(ValueError, forecast.set_score_interval, {'count': INCORRECT_VALUE,
                                                                         'unit': SCORE_INTERVAL_UNIT})
        self.assertRaises(ValueError, forecast.set_score_interval, {'count': SCORE_INTERVAL_COUNT,
                                                                         'unit': INCORRECT_VALUE})

    def test_set_range(self):
        forecast = ForecastTransformation()
        forecast.set_range(MIN_RANGE, MAX_RANGE)
        self.assertEqual({'min': MIN_RANGE, 'max': MAX_RANGE}, forecast.range)
        self.assertRaises(ValueError, forecast.set_range, INCORRECT_VALUE, MAX_RANGE)
        self.assertRaises(ValueError, forecast.set_range, MIN_RANGE, INCORRECT_VALUE)

    def test_set_holtwinters(self):
        forecast = ForecastTransformation()
        forecast.set_holtwinters(HOLTWINTERS)
        self.assertEqual(HOLTWINTERS, forecast.hw)
        self.assertRaises(ValueError, forecast.set_holtwinters, INCORRECT_VALUE)

    def test_set_arima(self):
        forecast = ForecastTransformation()
        forecast.set_arima(ARIMA)
        self.assertEqual(ARIMA, forecast.arima)
        self.assertRaises(ValueError, forecast.set_arima, INCORRECT_VALUE)

    def test_set_ssa(self):
        forecast = ForecastTransformation()
        forecast.set_ssa(SSA)
        self.assertEqual(SSA, forecast.ssa)
        self.assertRaises(ValueError, forecast.set_ssa, INCORRECT_VALUE)

    def test_set_horizon(self):
        forecast = ForecastTransformation()
        forecast.set_horizon(HORIZON)
        self.assertEqual(HORIZON, forecast.horizon)
        self.assertRaises(ValueError, forecast.set_horizon, INCORRECT_VALUE)

    def test_set_baseline(self):
        forecast = ForecastTransformation()
        forecast.set_baseline(BASELINE)
        self.assertEqual(BASELINE, forecast.baseline)
        self.assertRaises(ValueError, forecast.set_baseline, INCORRECT_VALUE)
