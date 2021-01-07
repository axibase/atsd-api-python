# -*- coding: utf-8 -*-

"""
Copyright 2018 Axibase Corporation or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://www.axibase.com/atsd/axibase-apache-2.0.pdf

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""

from . import _jsonutil
from ._client import Client
from ._constants import *
from ._time_utilities import to_iso, to_date
from .exceptions import DataParseException, SQLException, ServerException
from .models import Series, Property, Alert, AlertHistory, Metric, Entity, EntityGroup, Message
from io import StringIO
from requests.compat import quote


def _check_name(name):
    if not isinstance(name, (bytes, str)):
        raise TypeError('name must be str or bytes')
    if len(name) == 0:
        raise ValueError('name is empty')


class _Service(object):
    def __init__(self, conn):
        if not isinstance(conn, Client):
            raise ValueError('conn must be Client instance')
        self.conn = conn


# ------------------------------------------------------------------------ SERIES
class SeriesService(_Service):
    def insert(self, *series_objects):
        """Insert an array of samples for a given series identified by metric, entity, and series tags

        :param series_objects: :class:`.Series` objects
        :return: True if success
        """
        for series in series_objects:
            if len(series.data) == 0:
                raise DataParseException('data', Series, 'Inserting empty series')
        self.conn.post(series_insert_url, series_objects)
        return True

    def query(self, *queries):
        """Retrieve series for each query

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

    def delete(self, *delete_query):
        """Delete series matching delete_query tuple

        :param delete_query: :class:`.SeriesDeleteQuery`
        :return: json with count of deleted series if success
        """
        try:
            response = self.conn.post(series_delete_url, delete_query)
        except ServerException as e:
            if e.status_code == 404:
                return e.content
            else:
                raise e
        return response


# -------------------------------------------------------------------- PROPERTIES
class PropertiesService(_Service):
    def insert(self, *properties):
        """Insert given properties

        :param properties: :class:`.Property`
        :return: True if success
        """
        self.conn.post(properties_insert_url, properties)
        return True

    def query(self, *queries):
        """Retrieves property records for each query

        :param queries: :class:`.PropertiesQuery`
        :return: list of :class:`.Property` objects
        """
        resp = self.conn.post(properties_query_url, queries)
        return _jsonutil.deserialize(resp, Property)

    def query_dataframe(self, *queries, **frame_params):
        """Retrieve Property records as DataFrame

        :param queries: :class: `.PropertiesQuery`
        :param frame_params: parameters for DataFrame constructor, for example, columns=['entity', 'tags', 'message']
        :param expand_tags: `bool` If True response key and tags are converted to columns. Default: True
        :return: :class:`.DataFrame`
        """
        resp = self.conn.post(properties_query_url, queries)
        reserved = {'type', 'entity', 'tags', 'key', 'date'}
        return response_to_dataframe(resp, reserved, **frame_params)

    def type_query(self, entity):
        """Returns an array of property types for the entity.

        :param entity: :class:`.Entity`
        :return: returns `list` of property types for the entity.
        """
        entity_name = entity.name if isinstance(entity, Entity) else entity
        response = self.conn.get(properties_types_url.format(entity=quote(entity_name, '')))
        return response

    def url_query(self, entity_name, property_type):
        """Retrieves Properties of the given type for the given entity
        
        :param entity_name: :class: `str`
        :param property_type: :class: `str`
        :return: list of :class: `.Property`
        """
        response = self.conn.get(properties_url_query_url.format(entity=entity_name, type=property_type))
        return _jsonutil.deserialize(response, Property)

    def delete(self, *filters):
        """Delete properties for each query

        :param filters: :class:`.PropertiesDeleteQuery`
        :return: True if success
        """
        response = self.conn.post(properties_delete_url, filters)
        return True


# ------------------------------------------------------------------------ ALERTS
class AlertsService(_Service):
    def query(self, *queries):
        """Retrieve alert records for each query

        :param queries: :class:`.AlertsQuery`
        :return: get of :class:`.Alert` objects
        """
        resp = self.conn.post(alerts_query_url, queries)
        return _jsonutil.deserialize(resp, Alert)

    def update(self, *updates):
        """Change acknowledgement status for the specified open alerts.

        :param updates: `dict`
        :return: True if success
        """
        response = self.conn.post(alerts_update_url, updates)
        return True

    def history_query(self, *queries):
        """Retrieve alert history for each query

        :param queries: :class:`.AlertHistoryQuery`
        :return: get of :class:`.AlertHistory` objects
        """
        resp = self.conn.post(alerts_history_url, queries)
        return _jsonutil.deserialize(resp, AlertHistory)

    def delete(self, *ids):
        """Delete alerts by id

        :param ids: `int`
        :return: True if success
        """
        response = self.conn.post(alerts_delete_url, ids)
        return True


# ---------------------------------------------------------------------- MESSAGES
class MessageService(_Service):
    def insert(self, *messages):
        """Insert specified messages

        :param messages: :class:`.Message`
        :return: True if success
        """
        response = self.conn.post(messages_insert_url, messages)
        return True

    def query(self, *queries):
        """Retrieve messages for each query

        :param queries: :class:`.MessageQuery`
        :return: `list` of :class:`.Message` objects
        """
        resp = self.conn.post(messages_query_url, queries)
        return _jsonutil.deserialize(resp, Message)

    def query_dataframe(self, *queries, **frame_params):
        """Retrieve Message records as DataFrame

        :param queries: :class: `.MessageQuery`
        :param frame_params: parameters for DataFrame constructor, for example, columns=['entity', 'tags', 'message']
        :param expand_tags: `bool` If True response tags are converted to columns. Default: True
        :return: :class:`.DataFrame`
        """
        resp = self.conn.post(messages_query_url, queries)
        reserved = {'type', 'entity', 'tags', 'source', 'date', 'message', 'severity'}
        return response_to_dataframe(resp, reserved, **frame_params)

    def statistics(self, *params):
        """
        Unimplemented
        """
        raise NotImplementedError


# ===============================================================================
#################################  META   #####################################
# ===============================================================================

# ----------------------------------------------------------------------- METRICS
class MetricsService(_Service):
    def get(self, name):
        """Retrieve metric.

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

    def list(self, expression=None, min_insert_date=None, max_insert_date=None, tags=None, limit=None):
        """Retrieve a `list` of metrics matching the specified filters.

        :param expression: `str`
        :param min_insert_date: `int` | `str` | None | :class:`datetime`
        :param max_insert_date: `int` | `str` | None | :class:`datetime`
        :param tags: `str`
        :param limit: `int`
        :return: :class:`.Metric` objects
        """
        params = {}
        if expression is not None:
            params['expression'] = expression
        if min_insert_date is not None:
            params['minInsertDate'] = to_iso(min_insert_date)
        if max_insert_date is not None:
            params['maxInsertDate'] = to_iso(max_insert_date)
        if tags is not None:
            params['tags'] = tags
        if limit is not None:
            params['limit'] = limit
        response = self.conn.get(metric_list_url, params)
        return _jsonutil.deserialize(response, Metric)

    def update(self, metric):
        """Update the specified metric.

        :param metric: :class:`.Metric`
        :return: True if success
        """
        self.conn.patch(metric_update_url.format(metric=quote(metric.name, '')), metric)
        return True

    def create_or_replace(self, metric):
        """Create a metric or replace an existing metric.

        :param metric: :class:`.Metric`
        :return: True if success
        """
        self.conn.put(metric_create_or_replace_url.format(metric=quote(metric.name, '')), metric)
        return True

    def delete(self, metric_name):
        """Delete the specified metric.

        :param metric_name: :class:`.Metric`
        :return: True if success
        """
        self.conn.delete(metric_delete_url.format(metric=quote(metric_name, '')))
        return True

    def series(self, metric, entity=None, tags=None, min_insert_date=None, max_insert_date=None):
        """Retrieve series for the specified metric.

        :param metric: `str` | :class:`.Metric`
        :param entity: `str` | :class:`.Entity`
        :param tags: `dict`
        :param min_insert_date: `int` | `str` | None | :class:`datetime`
        :param max_insert_date: `int` | `str` | None | :class:`datetime`

        :return: :class:`.Series`
        """
        metric_name = metric.name if isinstance(metric, Metric) else metric
        _check_name(metric_name)

        params = {}
        if entity is not None:
            params['entity'] = entity.name if isinstance(entity, Entity) else entity
        if tags is not None and isinstance(tags, dict):
            for k, v in tags.items():
                params['tags.%s' % k] = v
        if min_insert_date is not None:
            params['minInsertDate'] = to_iso(min_insert_date)
        if max_insert_date is not None:
            params['maxInsertDate'] = to_iso(max_insert_date)

        try:
            response = self.conn.get(metric_series_url.format(metric=quote(metric_name, '')),
                                     params)
        except ServerException as e:
            if e.status_code == 404:
                return []
            else:
                raise e
        return _jsonutil.deserialize(response, Series)


# ---------------------------------------------------------------------- ENTITIES
class EntitiesService(_Service):
    def get(self, entity_name):
        """Retrieve the entity

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

    def list(self, expression=None, min_insert_date=None, max_insert_date=None, tags=None, limit=None):
        """Retrieve a list of entities matching the specified filters.

        :param expression: `str`
        :param min_insert_date: `str` | `int` | :class:`datetime`
        :param max_insert_date: `str` | `int` | :class:`datetime`
        :param tags: `dict`
        :param limit: `int`
        :return: :class:`.Entity` objects
        """
        params = {}
        if expression is not None:
            params["expression"] = expression
        if min_insert_date is not None:
            params["minInsertDate"] = to_iso(min_insert_date)
        if max_insert_date is not None:
            params["maxInsertDate"] = to_iso(max_insert_date)
        if tags is not None:
            params["tags"] = tags
        if limit is not None:
            params["limit"] = limit
        resp = self.conn.get(ent_list_url, params)
        return _jsonutil.deserialize(resp, Entity)

    def query_dataframe(self, expression=None, min_insert_date=None,
                        max_insert_date=None, tags=None, limit=None, **frame_params):
        """Retrieve a list of entities matching specified filters as DataFrame.

        :param expression: `str`
        :param min_insert_date: `str` | `int` | :class:`datetime`
        :param max_insert_date: `str` | `int` | :class:`datetime`
        :param tags: `dict`
        :param limit: `int`
        :param frame_params: parameters for DataFrame constructor. For example, columns=['entity', 'tags', 'message']
        :param expand_tags: `bool` If True response tags are converted to columns. Default: True
        :return: :class:`.DataFrame`
        """
        params = {}
        if expression is not None:
            params["expression"] = expression
        if min_insert_date is not None:
            params["minInsertDate"] = to_iso(min_insert_date)
        if max_insert_date is not None:
            params["maxInsertDate"] = to_iso(max_insert_date)
        if tags is not None:
            params["tags"] = tags
        if limit is not None:
            params["limit"] = limit
        resp = self.conn.get(ent_list_url, params)
        reserved = {'name', 'tags', 'enabled', 'time_zone', 'interpolate', 'label', 'created_date', 'last_insert_date'}
        return response_to_dataframe(resp, reserved, **frame_params)

    def update(self, entity):
        """Update the specified entity.

        :param entity: :class:`.Entity`
        :return: True if success
        """
        self.conn.patch(ent_update_url.format(entity=quote(entity.name, '')), entity)
        return True

    def create_or_replace(self, entity):
        """Create an entity or update an existing entity.

        :param entity: :class:`.Entity`
        :return: True if success
        """
        self.conn.put(ent_create_or_replace_url.format(entity=quote(entity.name, '')), entity)
        return True

    def delete(self, entity):
        """Delete the specified entity.

        :param entity: :class:`.Entity` | `str` Entity name.
        :return: True if success
        """
        entity_name = entity.name if isinstance(entity, Entity) else entity
        self.conn.delete(ent_delete_url.format(entity=quote(entity_name, '')))
        return True

    def metrics(self, entity, expression=None, min_insert_date=None, max_insert_date=None, use_entity_insert_time=False,
                limit=None, tags=None):
        """Retrieve a `list` of metrics matching the specified filters.

        :param entity: `str` | :class:`.Entity`
        :param expression: `str`
        :param min_insert_date: `int` | `str` | None | :class:`datetime`
        :param max_insert_date: `int` | `str` | None | :class:`datetime`
        :param use_entity_insert_time: `bool` If true, last_insert_date is calculated for the specified entity and metric
        :param limit: `int`
        :param tags: `str`
        :return: :class:`.Metric` objects
        """
        entity_name = entity.name if isinstance(entity, Entity) else entity
        _check_name(entity_name)
        params = {}
        if expression is not None:
            params['expression'] = expression
        if min_insert_date is not None:
            params['minInsertDate'] = to_iso(min_insert_date)
        if max_insert_date is not None:
            params['maxInsertDate'] = to_iso(max_insert_date)
        params['useEntityInsertTime'] = use_entity_insert_time
        if limit is not None:
            params['limit'] = limit
        if tags is not None:
            params['tags'] = tags
        response = self.conn.get(ent_metrics_url.format(entity=quote(entity_name, '')), params)
        return _jsonutil.deserialize(response, Metric)


# ----------------------------------------------------------------- ENTITY GROUPS
class EntityGroupsService(_Service):
    def get(self, group_name):
        """Retrieve the specified entity group.

        :param group_name: `str` entity group name
        :return: :class:`.EntityGroup`
        """
        _check_name(group_name)
        try:
            resp = self.conn.get(eg_get_url.format(group=quote(group_name, '')))
        except ServerException as e:
            if e.status_code == 404:
                return None
            else:
                raise e
        return _jsonutil.deserialize(resp, EntityGroup)

    def list(self, expression=None, tags=None, limit=None):
        """Retrieve a list of entity groups.

        :param expression: `str` Expression to include entity groups by name or tags.
        :param tags: `dict` Comma-separated list of entity group tag names to be displayed in the response.
        :param limit: `int` Maximum number of entity groups to retrieve, ordered by name.
        :return: :class:`.EntityGroup` objects
        """
        params = {}
        if expression is not None:
            params["expression"] = expression
        if tags is not None:
            params["tags"] = tags
        if limit is not None:
            params["limit"] = limit
        resp = self.conn.get(eg_list_url, params)
        return _jsonutil.deserialize(resp, EntityGroup)

    def update(self, group):
        """Update the specified entity group.
        Unlike replace method, fields and tags not specified in the request remain unchanged.

        :param group: :class:`.EntityGroup`
        :return: True if success
        """
        self.conn.patch(eg_update_url.format(group=quote(group.name, '')), group)
        return True

    def create_or_replace(self, group):
        """Create an entity group or replace an existing entity group.

        :param group: :class:`.EntityGroup`
        :return: True if successful
        """
        self.conn.put(eg_create_or_replace_url.format(group=quote(group.name, '')), group)
        return True

    def delete(self, group):
        """Delete the specified entity group.
        Member entities and their data are not affected by this operation.

        :param group: :class:`.EntityGroup` | `str` Entity Group name.
        :return: True if success
        """
        group_name = group.name if isinstance(group, EntityGroup) else group
        self.conn.delete(eg_delete_url.format(group=quote(group_name, '')))
        return True

    def get_entities(self, group_name, expression=None, min_insert_date=None, max_insert_date=None, tags=None,
                     limit=None):
        """Retrieve a list of entities that are members of the specified entity group and match the specified expression filter.

        :param group_name: `str`
        :param expression: `str`
        :param min_insert_date: `str` | `int` | :class:`datetime`
        :param max_insert_date: `str` | `int` | :class:`datetime`
        :param tags: `dict`
        :param limit: `int`
        :return: `list` of :class:`.Entity` objects
        """
        _check_name(group_name)
        params = {}
        if expression is not None:
            params["expression"] = expression
        if min_insert_date is not None:
            params["minInsertDate"] = to_iso(min_insert_date)
        if max_insert_date is not None:
            params["maxInsertDate"] = to_iso(max_insert_date)
        if tags is not None:
            params["tags"] = tags
        if limit is not None:
            params["limit"] = limit
        resp = self.conn.get(eg_get_entities_url.format(group=quote(group_name, '')), params)
        return _jsonutil.deserialize(resp, Entity)

    def add_entities(self, group_name, entities, create_entities=None):
        """Add entities as members to the specified entity group.
        Changing members of expression-based groups is not supported.

        :param group_name: `str`
        :param entities: `list` of :class:`.Entity` objects | `list` of `str` entity names
        :param create_entities: `bool` option indicating new entities from the submitted list are created if such
        entities do not exist :return: True if success
        """
        _check_name(group_name)
        data = []
        for e in entities:
            data.append(e.name if isinstance(e, Entity) else e)
        params = {"createEntities": True if create_entities is None else create_entities}
        response = self.conn.post(eg_add_entities_url.format(group=quote(group_name, '')), data,
                                  params=params)
        return True

    def set_entities(self, group_name, entities, create_entities=None):
        """Set members of the entity group from the specified entity list.
        All existing members that are not included in the request are removed from members.
        If the array in the request is empty, all entities are removed from the group and are replaced with an empty list.
        Changing members of expression-based groups is not supported.

        :param group_name: `str`
        :param entities: `list` of :class:`.Entity` objects | `list` of `str` entity names 
        :param create_entities: `bool` option indicating if new entities from the submitted list is created if such entities don't exist
        :return: True if success
        """
        _check_name(group_name)
        data = []
        for e in entities:
            data.append(e.name if isinstance(e, Entity) else e)
        params = {"createEntities": True if create_entities is None else create_entities}
        response = self.conn.post(eg_set_entities_url.format(group=quote(group_name, '')), data,
                                  params=params)
        return True

    def delete_entities(self, group_name, entities):
        """Remove specified entities from members of the specified entity group.
        To delete all entities, submit an empty list [] using the set_entities method.
        Changing members of expression-based groups is not supported.

        :param group_name: `str`
        :param entities: `list` of :class:`.Entity` objects | `list` of `str` entity names
        :return: True if success
        """
        _check_name(group_name)
        data = []
        for e in entities:
            data.append(e.name if isinstance(e, Entity) else e)

        response = self.conn.post(eg_delete_entities_url.format(group=quote(group_name, '')),
                                  data=data)
        return True


# --------------------------------------------------------------------------- SQL
class SQLService(_Service):
    def query(self, sql_query):
        """Execute SQL query.

        :param sql_query: `str`
        :return: :class:`.DataFrame` object
        """
        response = self.query_with_params(sql_query)
        import pandas as pd
        pd.set_option("display.expand_frame_repr", False)
        return pd.read_csv(StringIO(response), sep=',')

    def query_with_params(self, sql_query, params=None):
        """Execute SQL query with api parameters.

        :param sql_query: `str`
        :param params: `dict`
        :return: Content of the response
        """
        if params is None:
            params = {'outputFormat': 'csv'}
        params['q'] = sql_query
        try:
            response_text = self.conn.post(sql_query_url, None, params)
        except ServerException as e:
            if e.status_code == 404:
                return None
            else:
                raise SQLException(e.status_code, e.content, sql_query)
        return response_text

    def cancel_query(self, query_id):
        """Cancel the execution of the specified SQL query identified by query id.

        :param query_id: `str`
        :return: True if success
        """
        response = self.conn.get(sql_cancel_url, {'queryId': query_id})
        return True


# ---------------------------------------------------------------------- COMMANDS
class CommandsService(_Service):
    def send_commands(self, commands, commit=False):
        """Send a command or a batch of commands in Network API syntax via /api/v1/command

        :param commands: `str` | `list`
        :param commit: `bool` If True store the commands synchronously and return "stored" field in the response JSON.
        Default: False.
        :return: JSON with "fail","success" and "total" fields
        """
        if type(commands) is not list: commands = [commands]
        data = '\n'.join(commands)
        commit = 'true' if commit else 'false'
        url = commands_url + "?commit=" + commit
        response = self.conn.post_plain_text(url, data)
        return response


# ---------------------------------------------------------------------- PORTAL
class PortalsService(_Service):
    def get_portal(self, id=None, name=None, portal_file=None, entity=None, width=900, height=600, theme=None,
                   **kwargs):
        """Generates a screenshot of the specified portal in PNG format.

        :param id: `int` Portal identifier. Either id or name parameter must be specified. If both parameters are
        specified, id takes precedence.
        :param name: `str` Portal name.
        :param portal_file: `str` File name where portal to be saved.
        Default: {portal-name}[_{entity_name}]_{yyyymmdd}.png.
        :param entity: `str` Entity name. Required for template portals.
        :param width: `int`  Screenshot width, in pixels. Default: 900.
        :param height: `int` Screenshot height, in pixels. Default: 600.
        :param theme: str` Portal theme. Possible values: Default, Black. Default value is set in portal
        configuration.
        :param kwargs: `str` Additional request parameters are passed to the target portal
        and are accessible using the ${parameter_name} syntax.
        :return: PNG file
        """
        query_params = locals()
        del query_params['portal_file']
        del query_params['kwargs']
        if id is None and name is None:
            raise ValueError("Either id or name parameter must be specified.")

        possible_themes = ["default", "black"]
        if theme is not None:
            if theme.lower() not in possible_themes:
                raise ValueError("Unsupported theme, use one of: {}".format(", ".join(possible_themes)))

        if len(kwargs) > 0:
            query_params.update(kwargs)
        self.conn.get(portal_export, query_params, portal=True, portal_file=portal_file)


def response_to_dataframe(resp, reserved, **frame_params):
    expand_tags = frame_params.pop('expand_tags', True)
    enc_resp = []
    fields = ['tags', 'key']
    for el in resp:
        for field in fields:
            dictionary = el.pop(field, None)
            if dictionary is not None:
                for k, v in dictionary.items():
                    if (expand_tags and (k in reserved)) or not expand_tags:
                        k = '{}.{}'.format(field, k)
                    el[k] = v
        if 'date' in el:
            # Message or Property
            el['date'] = to_date(el['date'])
        else:
            # Entity
            el['createdDate'] = to_date(el['createdDate'])
            if 'lastInsertDate' in el:
                el['lastInsertDate'] = to_date(el['lastInsertDate'])
            if 'versionDate' in el:
                el['versionDate'] = to_date(el['versionDate'])
        enc_resp.append(el)
    import pandas as pd
    pd.set_option("display.expand_frame_repr", False)
    pd.set_option('max_colwidth', None if pd.__version__ >= '1' else -1)
    return pd.DataFrame(enc_resp, **frame_params)
