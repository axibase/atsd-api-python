def copy_not_empty_attrs(src, dst):
    if src is not None and dst is not None:
        for attribute in src.__dict__:
            value = getattr(src, attribute)
            if value:
                setattr(dst, attribute, value)


class NoneDict(dict):
    def __init__(self, args, **kwargs):
        self.update(args, **kwargs) if args is not None else None

    def __getitem__(self, key):
        return dict.get(self, key)


def set_if_type_is_valid(value, expected_type):
    if not isinstance(value, expected_type):
        raise ValueError("Expected a " + str(expected_type) + " found: " + str(type(value)))
    return value


def set_if_has_attr(attr_name, expected_attr_owner):
    if not hasattr(expected_attr_owner, attr_name):
        raise ValueError("Expected one of " + str(expected_attr_owner) + " attributes, found: " + str(attr_name))
    return attr_name
