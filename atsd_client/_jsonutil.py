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

import inspect
import numbers
import six


def serialize(target):
    if isinstance(target, dict):
        return dict([k, serialize(v)] for k, v in six.iteritems(target))
    elif isinstance(target, (list, tuple)):
        return [serialize(el) for el in target]
    elif isinstance(target, bool):
        return str(target).lower()
    elif isinstance(target, (six.text_type, six.binary_type, numbers.Number)):
        return target
    elif target is None:
        return None
    else:
        try:
            result = {}
            props = target.__dict__.keys()
            for prop in props:
                serialized_property = serialize(target.__dict__[prop])
                if serialized_property is not None:
                    result[prop] = serialized_property
            return result
        except AttributeError:
            raise ValueError(six.text_type(target) + ' could not be serialized')


def deserialize(target, model_class):
    if isinstance(target, (list, tuple)):
        return [deserialize(el, model_class) for el in target]
    try:
        args = inspect.getargspec(model_class.__init__).args
        args.remove('self')
        params = {}
        for attr in target:
            if attr in args:
                params[attr] = target[attr]
        result_object = model_class(**params)
        for attr in target:
            if attr not in args:
                setattr(result_object, attr, target[attr])
    except:
        raise ValueError(six.text_type(target) + ' could not be deserialized to ' + six.text_type(model_class))
    return result_object
