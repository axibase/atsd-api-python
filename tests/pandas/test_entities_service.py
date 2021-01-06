# -*- coding: utf-8 -*-

import time
from datetime import datetime
from atsd_client.models import Entity
from tests import ServiceTestBase

NAME = 'pyapi.entity_service_df.entity'
METRIC = 'pyapi.entity_service_df.metric'
LABEL = NAME.upper()
INTERPOLATE = 'LINEAR'
TIME_ZONE = 'US/Pacific'
ENABLED = True
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
EXPRESSION = 'name="{}"'.format(NAME)


class TestEntitiesService(ServiceTestBase):

    def setUp(self):
        """
        Create entity.
        """
        entity = Entity(NAME, label=LABEL, interpolate=INTERPOLATE, time_zone=TIME_ZONE, tags=TAGS)
        self.service.create_or_replace(entity)
        time.sleep(self.wait_time)

    def test_query_dataframe(self):
        result = self.service.query_dataframe(expression=EXPRESSION, tags=TAGS)
        # print(result)
        self.assertIsNotNone(result)
        self.assertEqual((1, 8), result.shape)
        self.assertTrue(isinstance(result.at[0, 'createdDate'], datetime))
        self.assertTrue(isinstance(result.at[0, 'versionDate'], datetime))
        self.assertTrue(result.at[0, 'enabled'])
        self.assertEqual(NAME, result.at[0, 'name'])
        self.assertEqual(TAG_VALUE, result.at[0, TAG])
        self.assertEqual(LABEL, result.at[0, 'label'])
        self.assertEqual(TIME_ZONE, result.at[0, 'timeZone'])
        self.assertEqual(INTERPOLATE, result.at[0, 'interpolate'])

    def tearDown(self):
        """
        Clean up ATSD.
        """
        self.service.delete(NAME)
