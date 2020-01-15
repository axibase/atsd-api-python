from ._interval import *


# ------------------------------------------------------------------------------
class StatisticalFunction:
    MIN = "MIN"
    MAX = "MAX"
    AVG = "AVG"
    SUM = "SUM"
    COUNT = "COUNT"
    FIRST = "FIRST"
    LAST = "LAST"
    DELTA = "DELTA"
    COUNTER = "COUNTER"
    MEDIAN = "MEDIAN"
    STANDARD_DEVIATION = "STANDARD_DEVIATION"
    MEDIAN_ABS_DEV = "MEDIAN_ABS_DEV"
    SLOPE = "SLOPE"
    INTERCEPT = "INTERCEPT"
    WAVG = "WAVG"
    WTAVG = "WTAVG"
    THRESHOLD_COUNT = "THRESHOLD_COUNT"
    THRESHOLD_DURATION = 'THRESHOLD_DURATION'
    THRESHOLD_PERCENT = 'THRESHOLD_PERCENT'
    MIN_VALUE_TIME = "MIN_VALUE_TIME"
    MAX_VALUE_TIME = "MAX_VALUE_TIME"
    VARIANCE = "VARIANCE"
    POPULATION_VARIANCE = "POPULATION_VARIANCE"


# ------------------------------------------------------------------------------
class SmoothType:
    AVG = "AVG"
    COUNT = "COUNT"
    SUM = "SUM"
    WAVG = "WAVG"
    WTAVG = "WTAVG"
    EMA = "EMA"


# ------------------------------------------------------------------------------
class DownsampleAlgorithm:
    DETAIL = "DETAIL"
    INTERPOLATE = "INTERPOLATE"


# ------------------------------------------------------------------------------
class EvaluateMode:
    STRICT = "STRICT"
    NOT_STRICT = "NOT_STRICT"


# ------------------------------------------------------------------------------
class DecomposeMethod:
    FULL = "FULL"
    TRUNCATED = "TRUNCATED"
    AUTO = "AUTO"


# ------------------------------------------------------------------------------
class ReconstructAveragingFunction:
    AVG = "AVG"
    MEDIAN = "MEDIAN"


# ------------------------------------------------------------------------------
class SsaForecastMethod:
    RECURRENT = "RECURRENT"
    VECTOR = "VECTOR"


# ------------------------------------------------------------------------------
class SsaForecastBase:
    RECONSTRUCTED = "RECONSTRUCTED"
    ORIGINAL = "ORIGINAL"


# ------------------------------------------------------------------------------
class SsaGroupAutoClusteringMethod:
    HIERARCHICAL = "HIERARCHICAL"
    XMEANS = "XMEANS"
    NOVOSIBIRSK = "NOVOSIBIRSK"


class Smooth:
    """
    Class representing transformation param 'smooth'
    """

    def __init__(self, smoothType, count=None, interval=None, minimumCount=None, incompleteValue=None):
        if smoothType is None:
            raise ValueError("Type is required parameter for Smooth")
        self.set_type(smoothType)
        if count is not None:
            self.set_count(count)
        if interval is not None:
            self.set_interval(interval)
        if minimumCount is not None:
            self.set_minimum_count(minimumCount)
        if incompleteValue is not None:
            self.set_incomplete_value(incompleteValue)

    def set_type(self, smooth_type):
        self.type = set_if_has_attr(smooth_type, SmoothType)

    def set_count(self, count):
        self.count = set_if_type_is_valid(count, numbers.Number)

    def set_interval(self, interval=None, count=None, unit=None):
        self.interval = set_if_interval(interval, count, unit)

    def set_minimum_count(self, minimum_count):
        self.minimumCount = set_if_type_is_valid(minimum_count, numbers.Number)

    def set_incomplete_value(self, incomplete_value):
        self.incompleteValue = set_if_type_is_valid(incomplete_value, str)


class Downsample:
    """
    Class representing transformation param 'downsample'
    """

    def __init__(self, algorithm=None, difference=None, ratio=None, gap=None):
        if algorithm is not None:
            self.set_algorithm(algorithm)
        if difference is not None:
            self.set_difference(difference)
        if ratio is not None:
            self.set_ratio(ratio)
        if gap is not None:
            self.set_gap(gap)

    def set_algorithm(self, algorithm):
        self.algorithm = set_if_has_attr(algorithm, DownsampleAlgorithm)

    def set_difference(self, difference):
        self.difference = set_if_type_is_valid(difference, numbers.Number)

    def set_ratio(self, ratio):
        self.ratio = set_if_type_is_valid(ratio, numbers.Number)

    def set_gap(self, gap=None, count=None, unit=None):
        self.gap = set_if_interval(gap, count, unit)


class Evaluate:
    """
    Class representing transformation param 'evaluate'
    """

    def __init__(self, mode=None, libs=None, expression=None, script=None, order=None, timezone=None):
        if mode is not None:
            self.set_mode(mode)
        if libs is not None:
            self.set_libs(libs)
        if expression is not None:
            self.set_expression(expression)
        if script is not None:
            self.set_script(script)
        if order is not None:
            self.set_order(order)
        if timezone is not None:
            self.set_timezone(timezone)

    def set_mode(self, mode):
        self.mode = set_if_has_attr(mode, EvaluateMode)

    def set_libs(self, libs):
        self.libs = [libs] if not isinstance(libs, list) else libs

    def set_expression(self, expression):
        self.expression = set_if_type_is_valid(expression, str)

    def set_script(self, script):
        self.script = set_if_type_is_valid(script, str)

    def set_order(self, order):
        self.order = set_if_type_is_valid(order, numbers.Number)

    def set_timezone(self, timezone):
        self.timezone = set_if_type_is_valid(timezone, str)


# =======================================================================
# Forecast Transformation
# =======================================================================
class ForecastTransformation:

    def __init__(self, autoAggregate=None, aggregationFunction=None, include=None, scoreInterval=None, min_range=None, max_range=None,
                    holtwinters=None, arima=None, ssa=None, horizon=None, baseline=None):
        if autoAggregate is not None:
            self.set_auto_aggregate(autoAggregate)
        if aggregationFunction is not None:
            self.set_aggregation_function(aggregationFunction)
        if include is not None:
            self.set_include(include)
        if scoreInterval is not None:
            self.set_score_interval(scoreInterval)
        if min_range is not None and max_range is not None:
            self.set_range(min_range, max_range)
        if holtwinters is not None:
            self.set_holtwinters(holtwinters)
        if arima is not None:
            self.set_arima(arima)
        if ssa is not None:
            self.set_ssa(ssa)
        if horizon is not None:
            self.set_horizon(horizon)
        if baseline is not None:
            self.set_baseline(baseline)

    def set_auto_aggregate(self, auto_aggregate):
        self.autoAggregate = set_if_type_is_valid(auto_aggregate, bool)

    def set_aggregation_function(self, aggregation_function):
        if not (hasattr(StatisticalFunction, aggregation_function) or aggregation_function.upper().startswith("PERCENTILE")):
            raise ValueError('Expected one of StatisticalFunction attributes or PERCENTILE, found: ' + str(aggregation_function))
        self.aggregationFunction = aggregation_function

    def set_include(self, include):
        self.include = [include] if not isinstance(include, list) else include

    def set_score_interval(self, score_interval=None, count=None, unit=None):
        self.scoreInterval = set_if_interval(score_interval, count, unit)

    def set_range(self, minRange, maxRange):
        if not isinstance(minRange, numbers.Number):
            raise ValueError('Expected min to be a number, found: ' + str(type(minRange)))
        if not isinstance(maxRange, numbers.Number):
            raise ValueError('Expected max to be a number, found: ' + str(type(maxRange)))
        self.range = {'min': minRange, 'max': maxRange}

    def set_holtwinters(self, holtwinters):
        self.hw = set_if_type_is_valid(holtwinters, HoltWinters)

    def set_arima(self, arima):
        self.arima = set_if_type_is_valid(arima, Arima)

    def set_ssa(self, ssa):
        self.ssa = set_if_type_is_valid(ssa, Ssa)

    def set_horizon(self, horizon):
        self.horizon = set_if_type_is_valid(horizon, Horizon)

    def set_baseline(self, baseline):
        self.baseline = set_if_type_is_valid(baseline, Baseline)


class HoltWinters:

    def __init__(self, auto=None, period=None, alpha=None, beta=None, gamma=None):
        if auto is not None:
            self.set_auto(auto)
        if period is not None:
            self.set_period(period)
        if alpha is not None:
            self.set_alpha(alpha)
        if beta is not None:
            self.set_beta(beta)
        if gamma is not None:
            self.set_gamma(gamma)

    def set_auto(self, auto):
        self.auto = set_if_type_is_valid(auto, bool)

    def set_period(self, period=None, count=None, unit=None):
        self.period = set_if_interval(period, count, unit)

    def set_alpha(self, alpha):
        self.alpha = set_if_type_is_valid(alpha, numbers.Number)

    def set_beta(self, beta):
        self.beta = set_if_type_is_valid(beta, numbers.Number)

    def set_gamma(self, gamma):
        self.gamma = set_if_type_is_valid(gamma, numbers.Number)


class Horizon:

    def __init__(self, interval=None, length=None, endDate=None, startDate=None):
        if interval is not None:
            self.set_interval(interval)
        if length is not None:
            self.set_length(length)
        if endDate is not None:
            self.set_end_date(endDate)
        if startDate is not None:
            self.set_start_date(startDate)

    def set_interval(self, interval=None, count=None, unit=None):
        self.interval = set_if_interval(interval, count, unit)

    def set_length(self, length):
        self.length = set_if_type_is_valid(length, numbers.Number)

    def set_end_date(self, endDate):
        self.endDate = set_if_type_is_valid(endDate, str)

    def set_start_date(self, startDate):
        self.startDate = set_if_type_is_valid(startDate, str)


class Arima:

    def __init__(self, auto=None, autoRegressionInterval=None, p=None, d=None):
        if auto is not None:
            self.set_auto(auto)
        if autoRegressionInterval is not None:
            self.set_auto_regression_interval(autoRegressionInterval)
        if p is not None:
            self.set_p(p)
        if d is not None:
            self.set_d(d)

    def set_auto(self, auto):
        self.auto = set_if_type_is_valid(auto, bool)

    def set_auto_regression_interval(self, auto_regression_interval=None, count=None, unit=None):
        self.autoRegressionInterval = set_if_interval(auto_regression_interval, count, unit)

    def set_p(self, p):
        self.p = set_if_type_is_valid(p, numbers.Number)

    def set_d(self, d):
        self.d = set_if_type_is_valid(d, numbers.Number)


class Baseline:

    def __init__(self, period=None, count=None, function=None):
        if period is not None:
            self.set_period(period)
        if count is not None:
            self.set_count(count)
        if function is not None:
            self.set_function(function)

    def set_period(self, period=None, count=None, unit=None):
        self.period = set_if_interval(period, count, unit)

    def set_count(self, count):
        self.count = set_if_type_is_valid(count, numbers.Number)

    def set_function(self, function):
        if not (hasattr(StatisticalFunction, function) or function.upper().startswith("PERCENTILE")):
            raise ValueError('Function expected to be one of StatisticalFunction attributes or PERCENTILE, but found: ' + function)
        self.function = function


class Ssa:

    def __init__(self, decompose=None, group=None, reconstruct=None, ssaForecast=None):
        if decompose is not None:
            self.set_decompose(decompose)
        if group is not None:
            self.set_group(group)
        if reconstruct is not None:
            self.set_reconstruct(reconstruct)
        if ssaForecast is not None:
            self.set_forecast(ssaForecast)

    def set_decompose(self, decompose):
        self.decompose = set_if_type_is_valid(decompose, Decompose)

    def set_reconstruct(self, reconstruct):
        self.reconstruct = set_if_type_is_valid(reconstruct, Reconstruct)

    def set_forecast(self, ssaForecast):
        self.forecast = set_if_type_is_valid(ssaForecast, SsaForecast)

    def set_group(self, group):
        self.group = set_if_type_is_valid(group, SsaGroup)


class Decompose:

    def __init__(self, eigentripleLimit=None, method=None, windowLength=None, singularValueThreshold=None):
        if eigentripleLimit is not None:
            self.set_eigentriple_limit(eigentripleLimit)
        if method is not None:
            self.set_method(method)
        if windowLength is not None:
            self.set_window_length(windowLength)
        if singularValueThreshold is not None:
            self.set_singular_value_threshold(singularValueThreshold)

    def set_eigentriple_limit(self, eigentripleLimit):
        self.eigentripleLimit = set_if_type_is_valid(eigentripleLimit, numbers.Number)

    def set_method(self, method):
        self.method = set_if_has_attr(method, DecomposeMethod)

    def set_window_length(self, windowLength):
        self.windowLength = set_if_type_is_valid(windowLength, numbers.Number)

    def set_singular_value_threshold(self, singularValueThreshold):
        self.singularValueThreshold = set_if_type_is_valid(singularValueThreshold, numbers.Number)


class Reconstruct:

    def __init__(self, averagingFunction=None, fourier=None):
        if averagingFunction is not None:
            self.set_averaging_function(averagingFunction)
        if fourier is not None:
            self.set_fourier(fourier)

    def set_averaging_function(self, averagingFunction):
        self.averagingFunction = set_if_has_attr(averagingFunction, ReconstructAveragingFunction)

    def set_fourier(self, fourier):
        self.fourier = set_if_type_is_valid(fourier, bool)


class SsaForecast:

    def __init__(self, method=None, base=None):
        if method is not None:
            self.set_method(method)
        if base is not None:
            self.set_base(base)

    def set_method(self, method):
        self.method = set_if_has_attr(method, SsaForecastMethod)

    def set_base(self, base):
        self.base = set_if_has_attr(base, SsaForecastBase)


class SsaGroup:

    def __init__(self, auto=None, manual=None):
        if auto is not None:
            self.set_auto(auto)
        if manual is not None:
            self.set_manual(manual)

    def set_auto(self, auto):
        self.auto = set_if_type_is_valid(auto, SsaGroupAuto)

    def set_manual(self, manual):
        self.manual = set_if_type_is_valid(manual, SsaGroupManual)


class SsaGroupAuto:

    def __init__(self, count=None, stack=None, union=None, clustering=None):
        if count is not None:
            self.set_count(count)
        if stack is not None:
            self.set_stack(stack)
        if union is not None:
            self.set_union(union)
        if clustering is not None:
            self.set_clustering(clustering)

    def set_count(self, count):
        self.count = set_if_type_is_valid(count, numbers.Number)

    def set_stack(self, stack):
        self.stack = set_if_type_is_valid(stack, bool)

    def set_union(self, union):
        self.union = set_if_type_is_valid(union, list)

    def set_clustering(self, clustering):
        self.clustering = set_if_type_is_valid(clustering, SsaGroupAutoClustering)


class SsaGroupAutoClustering:

    def __init__(self, method=None, params=None):
        if method is not None:
            self.set_method(method)
        if params is not None:
            self.set_params(params)

    def set_method(self, method):
        self.method = set_if_has_attr(method, SsaGroupAutoClusteringMethod)

    def set_params(self, params):
        self.params = set_if_type_is_valid(params, dict)


class SsaGroupManual:

    def __init__(self, groups=None):
        if groups is not None:
            self.set_groups(groups)

    def set_groups(self, groups):
        self.groups = set_if_type_is_valid(groups, list)
