# -*- coding: utf-8 -*-

"""
Copyright 2015 Axibase Corporation or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://www.axibase.com/atsd/axibase-apache-2.0.pdf

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""

from .models import Series, Property, Alert, AlertHistory, Metric, Entity, EntityGroup, Message
from .exceptions import DataParseException
from .exceptions import ServerException
from ._client import Client
from . import _jsonutil
from ._constants import *
from ._time_utilities import to_iso_utc

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
try:
    unicode = unicode
except NameError:
    unicode = str


def _check_name(name):
    if not isinstance(name, (str, unicode)):
        raise TypeError('name should be str')
    if len(name) == 0:
        raise ValueError('name is empty')


class _Service(object):
    def __init__(self, conn):
        if not isinstance(conn, Client):
            raise ValueError('conn should be Client instance')
        self.conn = conn

#------------------------------------------------------------------------ SERIES
class SeriesService(_Service):
    def insert(self, *series_objects):
        """
        :param series_objects: :class:`.Series` objects
        :return: True if success
        """
        for series in series_objects:
            if len(series.data) == 0:
                raise DataParseException('data', Series, 'Inserting empty series')
        self.conn.post('series/insert', series_objects)
        return True
    
    def query(self, *queries):
        """
        Retrieve series for each query
        :param queries: :class:`.SeriesQuery` objects
        :return: list of :class:`.Series` objects
        """
        response = self.conn.post(series_query_url, queries)
        return [_jsonutil.deserialize(element, Series) for element in response]

    def url_query(self, *queries):
        """
        Unimplemented
        """
        raise NotImplementedError
    
    def csv_insert(self, *csvs):
        """
        Unimplemented
        """
        raise NotImplementedError

#-------------------------------------------------------------------- PROPERTIES
class PropertiesService(_Service):
    def insert(self, *properties):
        """
        Inserts given properties
        :param properties: :class:`.Property`
        :return: True if success
        """
        self.conn.post(properties_insert_url, properties)
        return True
    
    def query(self, *queries):
        """
        Retrieves property for each query
        :param queries: :class:`.PropertiesQuery`
        :return: list of :class:`.Property` objects
        """
        resp = self.conn.post(properties_query_url, queries)
        return _jsonutil.deserialize(resp, Property)
    
    def type_query(self, entity):
        """
        :param entity: :class:`.Entity`
        :return: returns `list` of property types for the entity.
        """
        response = self.conn.get(properties_types_url.format(entity=quote(entity.name, '')))
        return response

    def url_query(self, *queries):
        """
        Unimplemented 
        """
        raise NotImplementedError
    
    def delete(self, *filters):
        """
        Delete properties for each query
        :param filters: :class:`.PropertyDeleteFilter`
        :return: True if success
        """
        response = self.conn.post(properties_delete_url, filters)
        return True

#------------------------------------------------------------------------ ALERTS
class AlertsService(_Service):
    def query(self, *queries):
        """
        Retrieve alert for each query
        :param queries: :class:`.AlertsQuery`
        :return: get of :class:`.Alert` objects
        """
        resp = self.conn.post(alerts_query_url, queries)
        return _jsonutil.deserialize(resp, Alert)
    
    def update(self, *updates):
        """
        Change acknowledgement status of the specified open alerts.
        :param updates: `dict`
        :return: True if success
        """
        response = self.conn.post(alerts_update_url, updates)
        return True

    def history_query(self, *queries):
        """
        Retrieve history for each query
        :param queries: :class:`.AlertHistoryQuery`
        :return: get of :class:`.AlertHistory` objects
        """
        resp = self.conn.post(alerts_history_url, queries)
        return _jsonutil.deserialize(resp, AlertHistory)

    def delete(self, *ids):
        """
        Retrieve alert for each query
        :param id: `int`
        :return: True if success
        """
        response = self.conn.post(alerts_delete_url, ids)
        return True

#---------------------------------------------------------------------- MESSAGES
class MessageService(_Service):
    def insert(self, *messages):
        """
        Insert specified messages
        :param messages: :class:`.Message`
        :return: True if success
        """
        resp = self.conn.post(messages_insert_url, messages)
        return True
    
    def query(self, *queries):
        """
        Retrieve alerts for each query
        :param queries: :class:`.AlertsQuery`
        :return: `list` of :class:`.Alert` objects
        """
        resp = self.conn.post(messages_query_url, queries)
        return _jsonutil.deserialize(resp, Message)

    def statistics(self, *params):
        """
        Unimplemented
        """
        raise NotImplementedError


#===============================================================================
#################################  META   #####################################
#===============================================================================

#----------------------------------------------------------------------- METRICS
class MetricsService(_Service):
    def get(self, name):
        """
        Retrieve properties and tags for the specified metric.
        :param name: `str` metric name
        :return: :class:`.Metric`
        """
        _check_name(name)
        try:
            response = self.conn.get(metric_get_url.format(metric=quote(name, '')))
        except ServerException as e:
            if e.status_code == 404:
                return None
            else:
                raise e
        return _jsonutil.deserialize(response, Metric)

    def list(self, expression=None, minInsertDate=None, maxInsertDate=None, tags=None, limit=None):
        """
        Retrieve a `list` of metrics matching the specified filter conditions.
        :param expression: `str`
        :param minInsertDate: `int` | `str` | None | :class: `.datetime`
        :param maxInsertDate: `int` | `str` | None | :class: `.datetime`
        :param tags: `str`
        :param limit: `int`
        :return: :class:`.Metric` objects
        """
        params = {}
        if expression is not None:
            params['expression'] = expression
        if minInsertDate is not None:
            params['minInsertDate'] = to_iso_utc(minInsertDate)
        if maxInsertDate is not None:
            params['maxInsertDate'] = to_iso_utc(maxInsertDate)
        if tags is not None:
            params['tags'] = tags
        if limit is not None:
            params['limit'] = limit
        response = self.conn.get(metric_list_url, params)
        return _jsonutil.deserialize(response, Metric)
    
    def update(self, metric):
        """
        Update fields and tags of the specified metric.
        :param metric: :class: `.Metric`
        :return: True if success
        """
        self.conn.patch(metric_update_url.format(metric=quote(metric.name, '')), metric)
        return True
    
    def create_or_replace(self, metric):
        """
        Create a metric with specified fields and tags or replace the fields and tags of an existing metric.
        :param metric: :class:`.Metric`
        :return: True if success
        """
        self.conn.put(metric_create_or_replace_url.format(metric=quote(metric.name, '')), metric)
        return True


    def delete(self, metric_name):
        """
        Delete the specified metric.
        :param metric_name: :class:`.Metric`
        :return: True if success
        """
        self.conn.delete(metric_delete_url.format(metric=quote(metric_name, '')))
        return True

#------------------------------------------------------------------------------ ENTITIES
class EntitiesService(_Service):
    def get(self, entity_name):
        """
        Retrieve information about the specified entity including its tags.
        :param entity_name: `str` entity name
        :return: :class:`.Entity`
        """
        _check_name(entity_name)
        try:
            response = self.conn.get(ent_get_url.format(entity=quote(entity_name, '')))
        except ServerException as e:
            if e.status_code == 404:
                return None
            else:
                raise e
        return _jsonutil.deserialize(response, Entity)
    
    def list(self, expression=None, minInsertDate=None, maxInsertDate=None, tags=None, limit=None):
        """
        Retrieve a list of entities matching the specified filter conditions.
        :param expression: `str`
        :param minInsertDate: `str` | `int` | :class: `.datetime`  
        :param maxInsertDate: `str` | `int` | :class: `.datetime`
        :param tags: `dict`
        :param limit: `int`
        :return: :class:`.Entity` objects
        """
        params = dict()
        if expression is not None: 
             params["expression"] = expression
        if minInsertDate is not None: 
             params["minInsertDate"] = to_iso_utc(minInsertDate)
        if maxInsertDate is not None: 
             params["maxInsertDate"] = to_iso_utc(maxInsertDate)
        if tags is not None: 
             params["tags"] = tags
        if limit is not None: 
             params["limit"] = limit
        resp = self.conn.get(ent_list_url, params)
        return _jsonutil.deserialize(resp, Entity)

    def update(self, entity):
        """
        Update fields and tags of the specified entity.
        :param entity: :class:`.Entity`
        :return: True if success
        """
        self.conn.patch(ent_update_url.format(entity=quote(entity.name, '')), entity)
        return True

    def create_or_replace(self, entity):
        """
        Create an entity with specified fields and tags or replace the fields and tags of an existing entity.
        :param entity: :class:`.Entity`
        :return: True if success
        """
        self.conn.put(ent_create_or_replace_url.format(entity=quote(entity.name, '')), entity)
        return True

    def delete(self, entity):
        """
        Delete the specified entity and delete it as member from any entity groups that it belongs to.
        :param entity: :class:`.Entity`
        :return: True if success
        """
        self.conn.delete(ent_delete_url.format(entity=quote(entity.name, '')))
        return True

#------------------------------------------------------------------------------ ENTITIY GROUPS
class EntityGroupsService(_Service):
    def get(self, group_name):
        """
        Retrieve information about the specified entity group including its tags.
        Membership in entity groups with non-empty expression is managed by the server.
        Adding/removing members of expression-based groups is not supported.
        :param group_name: `str` entity group name
        :return: :class:`.EntityGroup`
        """
        _check_name(group_name)
        try:
            resp = self.conn.get('entity-groups/' + quote(group_name, ''))
        except ServerException as e:
            if e.status_code == 404:
                return None
            else:
                raise e
        return _jsonutil.deserialize(resp, EntityGroup)
    
    def list(self, expression=None, tags=None, limit=None):
        """
        Retrieve a list of entity groups.
        Membership in entity groups with non-empty expression is managed by the server. 
        Adding/removing members of expression-based groups is not supported.
        :param expression: `str`
        :param tags: `dict`
        :param limit: `int`
        :return: :class:`.EntityGroup` objects
        """
        params=dict()
        if expression is not None: 
             params["expression"] = expression
        if tags is not None: 
             params["tags"] = tags
        if limit is not None: 
             params["limit"] = limit
        resp = self.conn.get(eg_list_url, params)
        return _jsonutil.deserialize(resp, EntityGroup)

    def update(self, group):
        """
        Update fields and tags of the specified entity group.
        Unlike the replace method, fields and tags that are not specified in the request are left unchanged.
        :param group: :class:`.EntityGroup`
        :return: True if success
        """
        self.conn.patch(eg_update_url.format(group=quote(group.name, '')), group)
        return True

    def create_or_replace(self, group):
        """
        Create an entity group with specified fields and tags or replace the fields and tags of an existing entity group.
        :param group: :class:`.EntityGroup`
        :return: True if success
        """
        self.conn.put(eg_create_or_replace_url.format(group=quote(group.name, '')), group)
        return True

    def delete(self, group):
        """
        Delete the specified entity group.
        Member entities and their data is not affected by this operation.
        :param group: :class:`.EntityGroup`
        :return: True if success
        """
        self.conn.delete(eg_delete_url.format(group=quote(group.name, '')))
        return True

    def get_entities(self, group_name, expression=None, minInsertDate=None, maxInsertDate=None, tags=None, limit=None):
        """
        Retrieve a list of entities that are members of the specified entity group and are matching the specified filter conditions.
        :param group_name: `str`
        :param expression: `str`
        :param minInsertDate: `str` | `int` | :class: `.datetime`  
        :param maxInsertDate: `str` | `int` | :class: `.datetime`
        :param tags: `dict`
        :param limit: `int`
        :return: `list` of :class:`.Entity` objects
        """
        _check_name(group_name)
        params = dict()
        if expression is not None: 
            params["expression"] = expression
        if minInsertDate is not None: 
            params["minInsertDate"] = to_iso_utc(minInsertDate)
        if maxInsertDate is not None: 
            params["maxInsertDate"] = to_iso_utc(maxInsertDate)
        if tags is not None: 
            params["tags"] = tags
        if limit is not None: 
            params["limit"] = limit
        resp = self.conn.get(eg_get_entities_url.format(group=quote(group_name, '')), params)
        return _jsonutil.deserialize(resp, Entity)

    def add_entities(self, group_name, entities, createEntities=None):
        """
        Add entities as members to the specified entity group.
        :param group_name: `str`
        :param entities: `list` of :class:`.Entity` objects | `list` of `str` entity names 
        :param createEntities: `bool` flag indicating if new entities from the submitted list will be created if such entities don't exist
        :return: True if success
        """
        _check_name(group_name)
        data = [e.name if isinstance(e, Entity) else e for e in entities]
        params={"createEntities": True if createEntities is None else createEntities}
        response = self.conn.post(eg_add_entities_url.format(group=quote(group_name, '')), data, params=params)
        return True

    def set_entities(self, group_name, entities, createEntities=None):
        """
        Set members of the entity group from the specified entity list.
        All existing members that are not included in the request will be removed from members.
        If the array in the request is empty, all entities are removed from the group and are replaced with an empty list.
        :param group_name: `str`
        :param entities: `list` of :class:`.Entity` objects | `list` of `str` entity names 
        :param createEntities: `bool` flag indicating if new entities from the submitted list will be created if such entities don't exist
        :return: True if success
        """
        _check_name(group_name)
        data = [e.name if isinstance(e, Entity) else e for e in entities]
        params={"createEntities": True if createEntities is None else createEntities}
        response = self.conn.post(eg_set_entities_url.format(group=quote(group_name, '')), data, params=params)
        return True
    
    def delete_entities(self, group_name, entities):
        """
        Remove specified entities from members of the specified entity group.
        To delete all entities, submit an empty list [] with set_entities method.
        :param group_name: `str`
        :param entities: `list` of :class:`.Entity` objects | `list` of `str` entity names 
        :return: True if success
        """
        _check_name(group_name)
        data = [e.name if isinstance(e, Entity) else e for e in entities]
        response = self.conn.post(eg_delete_entities_url.format(group=quote(group_name, '')), data=entities)
        return True
