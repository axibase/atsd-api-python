from unittest import TestCase
from atsd_client.models import Arima, TimeUnit, Interval

AUTO = True
INTERVAL_COUNT = 1
INTERVAL_UNIT = TimeUnit.DAY
INTERVAL = Interval(INTERVAL_COUNT, INTERVAL_UNIT)
INTERVAL_DICT = {'count': INTERVAL_COUNT, 'unit': INTERVAL_UNIT}
P = 1
D = 1

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestArima(TestCase):

    def test_init(self):
        arima = Arima(AUTO, INTERVAL, P, D)
        self.assertEqual(AUTO, arima.auto)
        self.assertEqual(INTERVAL, arima.autoRegressionInterval)
        self.assertEqual(P, arima.p)
        self.assertEqual(D, arima.d)

    def test_set_auto(self):
        arima = Arima()
        arima.set_auto(AUTO)
        self.assertEqual(AUTO, arima.auto)
        self.assertRaises(ValueError, arima.set_auto, INCORRECT_VALUE)

    def test_set_auto_regression_interval(self):
        arima = Arima()
        arima.set_auto_regression_interval(count=INTERVAL_COUNT, unit=INTERVAL_UNIT)
        self.assertEqual(INTERVAL_DICT, arima.autoRegressionInterval)
        self.assertRaises(ValueError, arima.set_auto_regression_interval, None, INCORRECT_VALUE, INTERVAL_UNIT)
        self.assertRaises(ValueError, arima.set_auto_regression_interval, None, INTERVAL_COUNT, INCORRECT_VALUE)

    def test_set_auto_regression_interval_dict(self):
        arima = Arima()
        arima.set_auto_regression_interval(INTERVAL)
        self.assertEqual(INTERVAL, arima.autoRegressionInterval)
        arima.set_auto_regression_interval(INTERVAL_DICT)
        self.assertEqual(INTERVAL_DICT, arima.autoRegressionInterval)
        self.assertRaises(ValueError, arima.set_auto_regression_interval, {'count': INTERVAL_COUNT,
                                                                                INCORRECT_VALUE: INTERVAL_UNIT})
        self.assertRaises(ValueError, arima.set_auto_regression_interval, {'count': INCORRECT_VALUE,
                                                                                'unit': INTERVAL_UNIT})
        self.assertRaises(ValueError, arima.set_auto_regression_interval, {'count': INTERVAL_COUNT,
                                                                                'unit': INCORRECT_VALUE})

    def test_set_p(self):
        arima = Arima()
        arima.set_p(P)
        self.assertEqual(P, arima.p)
        self.assertRaises(ValueError, arima.set_p, INCORRECT_VALUE)

    def test_set_d(self):
        arima = Arima()
        arima.set_d(D)
        self.assertEqual(D, arima.d)
