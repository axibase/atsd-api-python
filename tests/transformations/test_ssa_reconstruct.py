from unittest import TestCase
from atsd_client.models import Reconstruct, ReconstructAveragingFunction

FUNCTION = ReconstructAveragingFunction.AVG
FOURIER = True

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestReconstruct(TestCase):

    def test_init(self):
        reconstruct = Reconstruct(FUNCTION, FOURIER)
        self.assertEqual(FUNCTION, reconstruct.averagingFunction)
        self.assertEqual(FOURIER, reconstruct.fourier)

    def test_set_averaging_function(self):
        reconstruct = Reconstruct()
        reconstruct.set_averaging_function(FUNCTION)
        self.assertEqual(FUNCTION, reconstruct.averagingFunction)
        self.assertRaises(ValueError, reconstruct.set_averaging_function, INCORRECT_VALUE)

    def test_set_fourier(self):
        reconstruct = Reconstruct()
        reconstruct.set_fourier(FOURIER)
        self.assertEqual(FOURIER, reconstruct.fourier)
        self.assertRaises(ValueError, reconstruct.set_fourier, INCORRECT_VALUE)
