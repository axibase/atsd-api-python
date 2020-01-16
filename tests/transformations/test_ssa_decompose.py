from unittest import TestCase
from atsd_client.models import Decompose, DecomposeMethod

LIMIT = 1
METHOD = DecomposeMethod.AUTO
WINDOW_LENGTH = 1
SINGULAR_VALUE_THRESHOLD = 1

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestDecompose(TestCase):

    def test_init(self):
        decompose = Decompose(LIMIT, METHOD, WINDOW_LENGTH, SINGULAR_VALUE_THRESHOLD)
        self.assertEqual(LIMIT, decompose.eigentripleLimit)
        self.assertEqual(METHOD, decompose.method)
        self.assertEqual(WINDOW_LENGTH, decompose.windowLength)
        self.assertEqual(SINGULAR_VALUE_THRESHOLD, decompose.singularValueThreshold)

    def test_set_eigentriple_limit(self):
        decompose = Decompose()
        decompose.set_eigentriple_limit(LIMIT)
        self.assertEqual(LIMIT, decompose.eigentripleLimit)
        self.assertRaises(ValueError, decompose.set_eigentriple_limit, INCORRECT_VALUE)

    def test_set_method(self):
        decompose = Decompose()
        decompose.set_method(METHOD)
        self.assertEqual(METHOD, decompose.method)
        self.assertRaises(ValueError, decompose.set_method, INCORRECT_VALUE)

    def test_set_window_length(self):
        decompose = Decompose()
        decompose.set_window_length(WINDOW_LENGTH)
        self.assertEqual(WINDOW_LENGTH, decompose.windowLength)
        self.assertRaises(ValueError, decompose.set_window_length, INCORRECT_VALUE)

    def test_set_singular_value_threshold(self):
        decompose = Decompose()
        decompose.set_singular_value_threshold(SINGULAR_VALUE_THRESHOLD)
        self.assertEqual(SINGULAR_VALUE_THRESHOLD, decompose.singularValueThreshold)
        self.assertRaises(ValueError, decompose.set_singular_value_threshold, INCORRECT_VALUE)
