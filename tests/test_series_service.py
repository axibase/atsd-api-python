# -*- coding: utf-8 -*-

import random
import time
from datetime import datetime
from datetime import timedelta
from atsd_client import models
from atsd_client.exceptions import DataParseException
from atsd_client.models import AggregateType, SeriesFilter, EntityFilter, DateFilter, VersioningFilter, Aggregate, \
    TransformationFilter, Group, Rate, SampleFilter
from atsd_client.models import Series
from atsd_client.models import SeriesQuery
from atsd_client.models import TimeUnit, Sample

from service_test_base import ServiceTestBase

ENTITY = 'pyapi.entity'
METRIC = 'pyapi.metric'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
WAIT_TIME = 4
TEST_NAME = 'pyapi/test'
GROUP_NAME = TEST_NAME
VALUE = 33333
VERSION_METRIC = 'pyapi.versioning.metric'


def insert_series_sample(data_service, val=None, *vals):
    series = Series(ENTITY, METRIC)
    series.tags = {TAG: TAG_VALUE}
    series.add_samples(Sample(val, datetime.now()))
    if vals:
        for i, v in enumerate(vals):
            time.sleep(WAIT_TIME + 2)
            series.add_samples(Sample(v, datetime.now()))

    # print('insertion =', series)

    return data_service.insert(series)


class TestSeriesService(ServiceTestBase):

    def test_fields_match(self):
        """
        Check fields of Series model were set as expected.
        """
        sample = Sample(1, datetime.now())
        series = Series(ENTITY, METRIC, tags={TAG: TAG_VALUE})
        series.add_samples(sample)
        self.assertEqual(ENTITY, series.entity)
        self.assertEqual(METRIC, series.metric)
        self.assertEqual({TAG: TAG_VALUE}, series.tags)
        self.assertEqual([sample], series.data)

    def test_insert_retrieve_series(self):
        val = random.randint(0, VALUE - 1)

        insert_series_sample(self.service, val)
        time.sleep(WAIT_TIME + 2)

        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]})
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=now - timedelta(hours=1), end_date=now)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)

        series = self.service.query(query)
        # for s in series:
        #     print(s)

        self.assertIsNotNone(series)
        self.assertGreater(len(series), 0)

        s = series[0]
        self.assertIsInstance(s, Series)

        self.assertGreater(len(s.data), 0)
        self.assertEqual(s.get_last_value(), val)

    def test_aggregate_series(self):
        val = random.randint(0, VALUE - 1)

        insert_series_sample(self.service, val, val + 1)
        time.sleep(WAIT_TIME)

        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]})
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=now - timedelta(hours=1), end_date=now)
        aggr = Aggregate(period={'count': 10, 'unit': TimeUnit.SECOND}, types=[AggregateType.MAX, AggregateType.MIN])
        tf = TransformationFilter(aggregate=aggr)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, transformation_filter=tf)

        series = self.service.query(query)
        self.assertEqual(len(series), 2)

        if series[0].aggregate['type'] == 'MAX':
            max = series[0].get_last_value()
            min = series[1].get_last_value()
        else:
            min = series[0].get_last_value()
            max = series[1].get_last_value()

        self.assertGreaterEqual(max, min)

    def test_insert_retrieve_versioning(self):

        test_status = 'pyapi.status'
        now = datetime.now()

        series = Series(ENTITY, VERSION_METRIC)
        val = random.randint(0, VALUE - 1)
        series.add_samples(Sample(value=val, time=now - timedelta(seconds=2), version={'status': test_status}))

        sf = SeriesFilter(metric=VERSION_METRIC)
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=now - timedelta(hours=1), end_date=now)
        vf = VersioningFilter(versioned=True)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, versioning_filter=vf)

        successful = self.service.insert(series)
        time.sleep(WAIT_TIME)
        series, = self.service.query(query)
        # print(series)
        last_sample = series.data[-1]

        self.assertTrue(successful)
        self.assertEqual(last_sample.v, val)
        self.assertIsNotNone(last_sample.version)
        self.assertEqual(last_sample.version['status'], test_status)

    def test_series_data_field_empty(self):
        series = Series(entity=ENTITY,
                        metric=METRIC)
        series.tags = {TAG: TAG_VALUE}
        # print(series)

        with self.assertRaises(DataParseException) as cm:
            self.service.insert(series)

        self.assertEqual(cm.exception.non_parsed_field, 'data')

    def test_forecast(self):
        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]}, type=models.SeriesType.FORECAST)
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=now - timedelta(hours=1), end_date=now)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)

        series = self.service.query(query)
        self.assertEqual(series[0].type, models.SeriesType.FORECAST)

    def test_rate(self):
        v1 = 5
        v2 = 3
        insert_series_sample(self.service, v1, v2)
        time.sleep(WAIT_TIME + 2)

        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]})
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=now - timedelta(hours=1), end_date=now)
        tf = TransformationFilter(rate=Rate(counter=False))
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, transformation_filter=tf)

        series = self.service.query(query)
        self.assertEqual(int(series[0].get_last_value()), v2 - v1)

    def test_group(self):
        time.sleep(1)
        insert_series_sample(self.service, VALUE - 1)
        time.sleep(WAIT_TIME)

        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]})
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=now - timedelta(hours=1), end_date=now)
        tf = TransformationFilter(group=Group(type=AggregateType.COUNT, period={'count': 1, 'unit': TimeUnit.SECOND}))
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, transformation_filter=tf)

        series = self.service.query(query)
        self.assertEqual(series[0].get_last_value(), 1)

    def test_sample_filter(self):
        """
        Check sample filter.
        """
        insert_series_sample(self.service, None, 2, 3)
        time.sleep(WAIT_TIME)

        sf = SeriesFilter(metric=METRIC, tags={TAG: TAG_VALUE}, exact_match=True)
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date='now - 1 * MINUTE', end_date="now")
        vf = SampleFilter('Float.isNaN(value) OR value=2')
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, sample_filter=vf)
        series = self.service.query(query)
        # print(series)
        self.assertIsNotNone(series)
        self.assertEqual(1, len(series))
        s = series[0]
        self.assertIsInstance(s, Series)
        self.assertEqual(2, len(s.data))
        self.assertEqual(None, s.get_first_value())
        self.assertEqual(2, s.get_last_value())

    def test_large_insert(self):
        date = datetime.now()
        data = []
        for i in range(10 ** 6):
            data.append(Sample(1, date))
            date = date - timedelta(minutes=1)
        series_to_insert = Series(ENTITY, METRIC, data)
        self.service.insert(series_to_insert)
