import numbers
from ._data_queries import TimeUnit, set_if_has_attr, set_if_type_is_valid


def set_if_interval(interval=None, count=None, unit=None):
    if interval is not None and count is not None and unit is not None:
        raise ValueError("Interval must be specified either by count and unit pair, or by interval instance. "
                         "Found both specifications.")
    period = None
    if interval is not None:
        period = interval
    elif count is not None and unit is not None:
        period = Interval(count, unit)
    else:
        raise ValueError("Interval must be specified either by count and unit pair, or by interval instance.")
    if not is_interval(period):
        raise ValueError("Expected interval, found: " + str(period))
    return period


class Interval:

    def __init__(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Period count must be a number, found: ' + str(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid unit ' + str(unit))
        self.count = count
        self.unit = unit

    def __contains__(self, item):
        return hasattr(self, item)

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        if key.lower() == "count":
            self.count = set_if_type_is_valid(value, numbers.Number)
        elif key.lower() == "unit":
            self.unit = set_if_has_attr(value, TimeUnit)
        else:
            raise ValueError("Invalid name of Interval key: " + str(key))


def is_interval(obj):
    if not ((obj is not None) and all(key in obj for key in ("count", "unit"))):
        return False
    if not isinstance(obj["count"], numbers.Number):
        raise ValueError("Interval count must be a number, found: " + str(type(obj["count"])))
    if not hasattr(TimeUnit, obj["unit"]):
        raise ValueError("Interval unit must be one of TimeUnit, found: " + str(obj["unit"]))
    return True
