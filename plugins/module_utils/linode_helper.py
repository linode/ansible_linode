"""This module contains helper functions for various Linode modules."""

from linode_api4 import and_

def dict_select_spec(target, spec):
    """Returns a new dictionary that only selects the keys from target that are specified in spec"""

    return {key: target.get(key) for key in spec.keys()}

def dict_select_matching(d_1, d_2):
    """Returns copies of the given dictionaries with all non-shared keys removed"""

    new_d1 = {key: d_1.get(key) for key in d_2.keys() if key in d_1.keys()}
    new_d2 = {key: d_2.get(key) for key in d_1.keys() if key in d_2.keys()}

    return new_d1, new_d2

def filter_null_values(input_dict):
    """Returns a copy of the given dict with all keys containing null values removed"""
    return {key: value for key, value in input_dict.items() if value is not None}

def paginated_list_to_json(target_list):
    """Copies a PaginatedList to a new list containing JSON objects"""
    return [value._raw_json for value in target_list]

# There might be a better way to do this, but this works for now
def create_filter_and(obj, filter_dict):
    """Returns a filter statement that requires all keys in the dict are matched."""

    keys = list(filter_dict.keys())
    values = list(filter_dict.values())

    if len(keys) < 1:
        return None

    filter_statement = getattr(obj, keys[0]) == values[0]

    if len(keys) == 1:
        return filter_statement

    for key, value in filter_dict.items():
        filter_statement = and_(filter_statement, getattr(obj, key) == value)

    return filter_statement
