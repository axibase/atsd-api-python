from unittest import TestCase
from atsd_client.models import SsaGroupAuto, SsaGroupAutoClustering

COUNT = 1
STACK = True
UNION = ['union']
CLUSTERING = SsaGroupAutoClustering()

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestSsaGroupAuto(TestCase):

    def test_init(self):
        auto = SsaGroupAuto(COUNT, STACK, UNION, CLUSTERING)
        self.assertEqual(COUNT, auto.count)
        self.assertEqual(STACK, auto.stack)
        self.assertEqual(UNION, auto.union)
        self.assertEqual(CLUSTERING, auto.clustering)

    def test_set_count(self):
        auto = SsaGroupAuto()
        auto.set_count(COUNT)
        self.assertEqual(COUNT, auto.count)
        self.assertRaises(ValueError, auto.set_count, INCORRECT_VALUE)

    def test_set_stack(self):
        auto = SsaGroupAuto()
        auto.set_stack(STACK)
        self.assertEqual(STACK, auto.stack)
        self.assertRaises(ValueError, auto.set_stack, INCORRECT_VALUE)

    def test_set_union(self):
        auto = SsaGroupAuto()
        auto.set_union(UNION)
        self.assertEqual(UNION, auto.union)
        self.assertRaises(ValueError, auto.set_union, INCORRECT_VALUE)

    def test_set_clustering(self):
        auto = SsaGroupAuto()
        auto.set_clustering(CLUSTERING)
        self.assertEqual(CLUSTERING, auto.clustering)
        self.assertRaises(ValueError, auto.set_clustering, INCORRECT_VALUE)
