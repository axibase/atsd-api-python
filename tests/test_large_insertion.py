import datetime
import unittest
import collections
from atsd_client.models import Sample
from atsd_client import connect_url
from atsd_client._constants import series_insert_url
from atsd_client._jsonutil import serialize

ENTITY = "pyapi.large.insertion.entity"
METRIC = "pyapi.large.insertion.metric"
SAMPLE_VALUE = 1

date = datetime.datetime.now()


class OrderedQuery:

    def __init__(self, data, entity, metric, data_first=True):
        self.query = collections.OrderedDict()
        if data_first:
            self.query["data"] = data
        self.query["entity"] = entity
        self.query["metric"] = metric
        if not data_first:
            self.query["data"] = data

    def to_dict(self):
        return collections.OrderedDict([k, serialize(v)] for k, v in self.query.items())


class TestLargeInsertion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global date
        cls.connection = connect_url('https://localhost:8443', 'axibase', 'axibase')
        cls.data = []
        for i in range(10**6):
            cls.data.append(Sample(SAMPLE_VALUE, date))
            date = date - datetime.timedelta(minutes=1)
        print("Data prepared")

    def test_large_sample_data_first(self):
        query = OrderedQuery(self.data, ENTITY, METRIC)
        self.connection.post(series_insert_url, [query])

    def test_large_sample_data_after(self):
        query = OrderedQuery(self.data, ENTITY, METRIC, False)
        self.connection.post(series_insert_url, [query])
