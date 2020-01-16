from unittest import TestCase
from atsd_client.models import SsaForecast, SsaForecastMethod, SsaForecastBase

METHOD = SsaForecastMethod.RECURRENT
BASE = SsaForecastBase.ORIGINAL

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestSsaForecast(TestCase):

    def test_init(self):
        forecast = SsaForecast(METHOD, BASE)
        self.assertEqual(METHOD, forecast.method)
        self.assertEqual(BASE, forecast.base)

    def test_set_method(self):
        forecast = SsaForecast()
        forecast.set_method(METHOD)
        self.assertEqual(METHOD, forecast.method)
        self.assertRaises(ValueError, forecast.set_method, INCORRECT_VALUE)

    def test_set_base(self):
        forecast = SsaForecast()
        forecast.set_base(BASE)
        self.assertEqual(BASE, forecast.base)
        self.assertRaises(ValueError, forecast.set_base, INCORRECT_VALUE)
