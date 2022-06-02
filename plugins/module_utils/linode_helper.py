"""This module contains helper functions for various Linode modules."""
from typing import Tuple, Any, Optional, cast, Dict, Set

import linode_api4
from linode_api4 import and_, MappedObject, LKENodePool, LKENodePoolNode
from linode_api4.objects.filtering import Filter, FilterableAttribute, FilterableMetaclass


def dict_select_spec(target: dict, spec: dict) -> dict:
    """Returns a new dictionary that only selects the keys from target that are specified in spec"""

    return {key: target.get(key) for key in spec.keys()}


def dict_select_matching(d_1: dict, d_2: dict) -> Tuple[dict, dict]:
    """Returns copies of the given dictionaries with all non-shared keys removed"""

    new_d1 = {key: d_1.get(key) for key in d_2.keys() if key in d_1.keys()}
    new_d2 = {key: d_2.get(key) for key in d_1.keys() if key in d_2.keys()}

    return new_d1, new_d2


def filter_null_values(input_dict: dict) -> dict:
    """Returns a copy of the given dict with all keys containing null values removed"""
    return {key: value for key, value in input_dict.items() if value is not None}


def drop_empty_strings(input_dict: dict) -> dict:
    """Returns a copy of the given dict with all keys containing null and empty values removed"""
    return {key: value for key, value in input_dict.items() if value is not None and value != ''}


def paginated_list_to_json(target_list: list) -> list:
    """Copies a PaginatedList to a new list containing JSON objects"""
    return [value._raw_json for value in target_list]


# There might be a better way to do this, but this works for now
def create_filter_and(obj: FilterableMetaclass, filter_dict: dict) -> Optional[Filter]:
    """Returns a filter statement that requires all keys in the dict are matched."""

    keys = list(filter_dict.keys())
    values = list(filter_dict.values())

    if len(keys) < 1:
        return None

    filter_statement: Filter = cast(FilterableAttribute, getattr(obj, keys[0])) == values[0]

    if len(keys) == 1:
        return filter_statement

    for key, value in filter_dict.items():
        filter_statement = and_(filter_statement, cast(FilterableAttribute,
                                                       getattr(obj, key)) == value)

    return filter_statement


def mapping_to_dict(obj: Any) -> Any:
    """Recursively converts a mapping to a dict. This is useful for nested API responses."""

    if isinstance(obj, MappedObject):
        obj = obj.dict

    if isinstance(obj, dict):
        return {key: mapping_to_dict(value) for key, value in obj.items()}

    if isinstance(obj, list):
        return [mapping_to_dict(value) for value in obj]

    return obj


def handle_updates(obj: linode_api4.Base, params: dict, mutable_fields: set, register_func: Any):
    """Handles updates for a linode_api4 object"""

    obj._api_get()

    # Update mutable values
    should_update = False
    params = filter_null_values(params)

    for key, new_value in params.items():
        if not hasattr(obj, key):
            continue

        old_value = getattr(obj, key)

        if type(old_value) in {
            linode_api4.objects.linode.Type,
            linode_api4.objects.linode.Region,
            linode_api4.objects.linode.Image,
            linode_api4.objects.lke.KubeVersion
        }:
            old_value = old_value.id

        if new_value != old_value:
            if key in mutable_fields:
                setattr(obj, key, new_value)
                register_func('Updated {0}: "{1}" -> "{2}"'.
                                     format(key, old_value, new_value))

                should_update = True
                continue

            raise RuntimeError(
                'failed to update {} -> {}: {} is a non-updatable'
                ' field'.format(old_value, new_value, key))

    if should_update:
        obj.save()


def jsonify_node_pool(pool: LKENodePool) -> Dict[str, Any]:
    """Converts an LKENodePool into a JSON-compatible dict"""

    result = pool._raw_json

    result['nodes'] = [jsonify_node_pool_node(node) for node in pool.nodes]

    return result


def jsonify_node_pool_node(node: LKENodePoolNode) -> Dict[str, Any]:
    """Converts an LKENodePoolNode into a JSON-compatible dict"""

    return {
        'id': node.id,
        'instance_id': node.instance_id,
        'status': node.status,
    }


def validate_required(required_fields: Set[str], params: Dict[str, Any]):
    """Returns whether the given parameters contain all of the required fields specified."""

    has_missing_field = False
    missing_fields = []

    for field in required_fields:
        if field not in params:
            missing_fields.append(field)
            has_missing_field = True

    if has_missing_field:
        raise Exception("missing fields: {}".format(', '.join(missing_fields)))
