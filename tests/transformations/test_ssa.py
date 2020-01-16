from unittest import TestCase
from atsd_client.models import Ssa, Decompose, Reconstruct, SsaForecast, SsaGroup

DECOMPOSE = Decompose()
RECONSTRUCT = Reconstruct()
FORECAST = SsaForecast()
GROUP = SsaGroup()

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestSsa(TestCase):

    def test_init(self):
        ssa = Ssa(DECOMPOSE, GROUP, RECONSTRUCT, FORECAST)
        self.assertEqual(DECOMPOSE, ssa.decompose)
        self.assertEqual(RECONSTRUCT, ssa.reconstruct)
        self.assertEqual(FORECAST, ssa.forecast)
        self.assertEqual(GROUP, ssa.group)

    def test_set_decompose(self):
        ssa = Ssa()
        ssa.set_decompose(DECOMPOSE)
        self.assertEqual(DECOMPOSE, ssa.decompose)
        self.assertRaises(ValueError, ssa.set_decompose, INCORRECT_VALUE)

    def test_set_reconstruct(self):
        ssa = Ssa()
        ssa.set_reconstruct(RECONSTRUCT)
        self.assertEqual(RECONSTRUCT, ssa.reconstruct)
        self.assertRaises(ValueError, ssa.set_reconstruct, INCORRECT_VALUE)

    def test_set_forecast(self):
        ssa = Ssa()
        ssa.set_forecast(FORECAST)
        self.assertEqual(FORECAST, ssa.forecast)
        self.assertRaises(ValueError, ssa.set_forecast, INCORRECT_VALUE)

    def test_set_group(self):
        ssa = Ssa()
        ssa.set_group(GROUP)
        self.assertEqual(GROUP, ssa.group)
        self.assertRaises(ValueError, ssa.set_group, INCORRECT_VALUE)
