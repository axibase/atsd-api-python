from unittest import TestCase
from atsd_client.models import SsaGroupAutoClustering, SsaGroupAutoClusteringMethod

METHOD = SsaGroupAutoClusteringMethod.HIERARCHICAL
PARAMS = {"key": "value"}

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestSsaGroupAutoClustering(TestCase):

    def test_init(self):
        clustering = SsaGroupAutoClustering(METHOD, PARAMS)
        self.assertEqual(METHOD, clustering.method)
        self.assertEqual(PARAMS, clustering.params)

    def test_set_method(self):
        clustering = SsaGroupAutoClustering()
        clustering.set_method(METHOD)
        self.assertEqual(METHOD, clustering.method)
        self.assertRaises(ValueError, clustering.set_method, INCORRECT_VALUE)

    def test_set_params(self):
        clustering = SsaGroupAutoClustering()
        clustering.set_params(PARAMS)
        self.assertEqual(PARAMS, clustering.params)
        self.assertRaises(ValueError, clustering.set_params, INCORRECT_VALUE)
