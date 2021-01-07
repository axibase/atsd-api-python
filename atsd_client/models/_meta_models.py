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
from .._time_utilities import to_date, timediff_in_minutes
from .._utilities import NoneDict


# ------------------------------------------------------------------------------
class DataType(object):
    SHORT = 'SHORT'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    LONG = 'LONG'
    DOUBLE = 'DOUBLE'
    DECIMAL = 'DECIMAL'


# ------------------------------------------------------------------------------
class TimePrecision(object):
    SECONDS = 'SECONDS'
    MILLISECONDS = 'MILLISECONDS'


# ------------------------------------------------------------------------------
class InvalidAction(object):
    NONE = 'NONE'
    DISCARD = 'DISCARD'
    TRANSFORM = 'TRANSFORM'
    RAISE_ERROR = 'RAISE_ERROR'
    SET_VERSION_STATUS = 'SET_VERSION_STATUS'


# ------------------------------------------------------------------------------
class Interpolate(object):
    LINEAR = 'LINEAR'
    PREVIOUS = 'PREVIOUS'


# ------------------------------------------------------------------------------
class Metric(object):
    """
    Class representing a metric.
    Metrics are names assigned to numeric measurements, for example, temperature or speed.
    A time-indexed array of measurements for a given metric and entity is called a time-series (or simply series).
    Metrics describe what is being measured as well as control how incoming data must be validated, stored, and pruned.
    """

    def __init__(self,
                 name,
                 label=None,
                 enabled=None,
                 data_type=None,
                 persistent=None,
                 filter=None,
                 min_value=None,
                 max_value=None,
                 invalid_action=None,
                 description=None,
                 retention_days=None,
                 series_retention_days=None,
                 last_insert_date=None,
                 tags=None,
                 versioned=None,
                 interpolate=None,
                 units=None,
                 time_zone=None,
                 created_date=None
                 ):
        #: `str` metric name
        self._name = name
        #: `str`
        self._label = label
        #: `bool`
        self._enabled = enabled
        #: :class:`.DataType`
        self._dataType = data_type
        #: `bool` persistence status.
        # Non-persistent metrics are not stored in the database and are only processed by the rule engine
        self._persistent = persistent
        #: If filter is specified, series commands that do not satisfy the filter condition are discarded
        self._filter = filter
        #: `Number` minimum value for Invalid Action trigger
        self._minValue = min_value
        #: `Number` maximum value for Invalid Action trigger
        self._maxValue = max_value
        #: :class:`.InvalidAction`
        self._invalidAction = invalid_action
        #: `str` metric description
        self._description = description
        #: `Number` number of days to store the values for this metric in the database
        self._retentionDays = retention_days
        #: `Number` number of days after which lagging series are removed from the database
        self._seriesRetentionDays = series_retention_days
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date.
        # Last time a value is received for this metric by any series
        self._lastInsertDate = to_date(last_insert_date)
        #: `dict`
        self._tags = NoneDict(tags)
        #: `boolean` If set to true, enables versioning for the specified metric.
        # When metrics is versioned, the database retains the history of series value changes
        # for the same timestamp along with version_source and version_status
        self._versioned = versioned
        #: :class:`.InterpolateType`
        self._interpolate = interpolate
        #: `str` metric units
        self._units = units
        #: `str` entity timezone
        self._timeZone = time_zone
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date. Creation date for this metric
        self._createdDate = to_date(created_date)

    def __repr__(self):
        return "<METRIC name={name}, label={label}, description={des}, created_date={createdDate}>".format(
            name=self._name, label=self._label,
            des=self._description, createdDate=self._createdDate)

    # Getters and setters
    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def enabled(self):
        return self._enabled

    @property
    def data_type(self):
        return self._dataType

    @property
    def persistent(self):
        return self._persistent

    @property
    def filter(self):
        return self._filter

    @property
    def min_value(self):
        return self._minValue

    @property
    def max_value(self):
        return self._maxValue

    @property
    def invalid_action(self):
        return self._invalidAction

    @property
    def description(self):
        return self._description

    @property
    def retention_days(self):
        return self._retentionDays

    @property
    def series_retention_days(self):
        return self._seriesRetentionDays

    @property
    def last_insert_date(self):
        return self._lastInsertDate

    @property
    def tags(self):
        return self._tags

    @property
    def versioned(self):
        return self._versioned

    @property
    def interpolate(self):
        return self._interpolate

    @property
    def units(self):
        return self._units

    @property
    def time_zone(self):
        return self._timeZone

    @name.setter
    def name(self, value):
        self._name = value

    @label.setter
    def label(self, value):
        self._label = value

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @data_type.setter
    def data_type(self, value):
        self._dataType = value

    @property
    def created_date(self):
        return self._createdDate

    @persistent.setter
    def persistent(self, value):
        self._persistent = value

    @filter.setter
    def filter(self, value):
        self._filter = value

    @min_value.setter
    def min_value(self, value):
        self._minValue = value

    @max_value.setter
    def max_value(self, value):
        self._maxValue = value

    @invalid_action.setter
    def invalid_action(self, value):
        self._invalidAction = value

    @description.setter
    def description(self, value):
        self._description = value

    @retention_days.setter
    def retention_days(self, value):
        self._retentionDays = value

    @series_retention_days.setter
    def series_retention_days(self, value):
        self._seriesRetentionDays = value

    @tags.setter
    def tags(self, value):
        self._tags = NoneDict(value)

    @versioned.setter
    def versioned(self, value):
        self._versioned = value

    @interpolate.setter
    def interpolate(self, value):
        self._interpolate = value

    @units.setter
    def units(self, value):
        self._units = value

    @time_zone.setter
    def time_zone(self, value):
        self._timeZone = value

    def get_elapsed_minutes(self):
        """Return elapsed time in minutes between current time and last insert time for this metric.

        :return: Time in minutes
        """
        return timediff_in_minutes(self.last_insert_date)


# ------------------------------------------------------------------------------
class Entity(object):
    """
    Class representing an entity.
    Entities describe objects being monitored, such as servers, sensors, buildings etc.
    """

    def __init__(self, name, enabled=None, label=None, interpolate=None, time_zone=None, last_insert_date=None,
                 tags=None, created_date=None, version_date=None):
        #: `str` entity name
        self._name = name
        #: `str` entity label
        self._label = label
        #: :class:`.InterpolateType`
        self._interpolate = interpolate
        #: `str` entity timezone
        self._timeZone = time_zone
        #: `bool` enabled status. Incoming data is discarded for disabled entities
        self._enabled = enabled
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date.
        # Last time when a value is received by the database for this entity
        self._lastInsertDate = to_date(last_insert_date)
        #: `dict`
        self._tags = NoneDict(tags)
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date. Creation date for this entity
        self._createdDate = to_date(created_date)
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date. Timestamp of entity version
        self._versionDate = to_date(version_date)

    def __repr__(self):
        return "<Entity name={name}, label={label}, created_date={createdDate}, version_date={versionDate}, last_insert_date={lit}, tags={tags}>".format(
            name=self._name,
            label=self._label,
            createdDate=self._createdDate,
            versionDate=self._versionDate,
            lit=self._lastInsertDate,
            tags=self._tags)

    # Getters and setters
    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def interpolate(self):
        return self._interpolate

    @property
    def time_zone(self):
        return self._timeZone

    @property
    def enabled(self):
        return self._enabled

    @property
    def last_insert_date(self):
        return self._lastInsertDate

    @property
    def tags(self):
        return self._tags

    @property
    def created_date(self):
        return self._createdDate

    @property
    def version_date(self):
        return self._versionDate

    @name.setter
    def name(self, value):
        self._name = value

    @label.setter
    def label(self, value):
        self._label = value

    @interpolate.setter
    def interpolate(self, value):
        self._interpolate = value

    @time_zone.setter
    def time_zone(self, value):
        self._timeZone = value

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @tags.setter
    def tags(self, value):
        self._tags = NoneDict(value)

    def get_elapsed_minutes(self):
        """Return elapsed time in minutes between current time and last insert date for the entity.

        :return: Time in minutes
        """
        return timediff_in_minutes(self.last_insert_date)


# ------------------------------------------------------------------------------
class EntityGroup(object):
    """
    Class representing an entity group.
    """

    def __init__(self, name, expression=None, tags=None, enabled=None):
        #: `str` entity group name
        self._name = name
        #: `str` group membership expression.
        # The expression is applied to entities to automatically add/remove members of this group
        self._expression = expression
        #: `dict`
        self._tags = NoneDict(tags)
        #: `bool`
        self._enabled = enabled

    def __repr__(self):
        return "<EntityGroup name={name}, expression={expression}, tags={tags}>".format(name=self._name,
                                                                                        expression=self._expression,
                                                                                        tags=self._tags,
                                                                                        enabled=self._enabled)

    # Getters and setters
    @property
    def name(self):
        return self._name

    @property
    def expression(self):
        return self._expression

    @property
    def tags(self):
        return self._tags

    @property
    def enabled(self):
        return self._enabled

    @name.setter
    def name(self, value):
        self._name = value

    @expression.setter
    def expression(self, value):
        self._expression = value

    @tags.setter
    def tags(self, value):
        self._tags = NoneDict(value)

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
