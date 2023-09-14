"""This module contains helper functions for various Linode modules."""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, cast

import linode_api4
import polling
from linode_api4 import (
    ApiError,
    LinodeClient,
    LKENodePool,
    LKENodePoolNode,
    MappedObject,
    and_,
)
from linode_api4.objects.filtering import (
    Filter,
    FilterableAttribute,
    FilterableMetaclass,
)


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
    return {
        key: value for key, value in input_dict.items() if value is not None
    }


def drop_empty_strings(input_dict: dict) -> dict:
    """Returns a copy of the given dict with all keys containing null and empty values removed"""
    return {
        key: value
        for key, value in input_dict.items()
        if value is not None and value != ""
    }


def paginated_list_to_json(target_list: list) -> list:
    """Copies a PaginatedList to a new list containing JSON objects"""
    return [value._raw_json for value in target_list]


# There might be a better way to do this, but this works for now
def create_filter_and(
    obj: FilterableMetaclass, filter_dict: dict
) -> Optional[Filter]:
    """Returns a filter statement that requires all keys in the dict are matched."""

    keys = list(filter_dict.keys())
    values = list(filter_dict.values())

    if len(keys) < 1:
        return None

    filter_statement: Filter = (
        cast(FilterableAttribute, getattr(obj, keys[0])) == values[0]
    )

    if len(keys) == 1:
        return filter_statement

    for key, value in filter_dict.items():
        filter_statement = and_(
            filter_statement,
            cast(FilterableAttribute, getattr(obj, key)) == value,
        )

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


def handle_updates(
    obj: linode_api4.Base, params: dict, mutable_fields: set, register_func: Any
) -> Set[str]:
    """Handles updates for a linode_api4 object"""

    obj._api_get()

    # Update mutable values
    params = filter_null_values(params)

    put_request = {}
    result = set()

    for key, new_value in params.items():
        if not hasattr(obj, key):
            continue

        old_value = parse_linode_types(getattr(obj, key))

        if new_value != old_value:
            if key in mutable_fields:
                put_request[key] = new_value
                result.add(key)
                register_func(
                    'Updated {0}: "{1}" -> "{2}"'.format(
                        key, old_value, new_value
                    )
                )

                continue

            raise RuntimeError(
                "failed to update {} -> {}: {} is a non-updatable"
                " field".format(old_value, new_value, key)
            )

    if len(put_request.keys()) > 0:
        obj._client.put(type(obj).api_endpoint, model=obj, data=put_request)

    return result


def parse_linode_types(value: any) -> any:
    """Helper function for handle_updates.
    Parses Linode Object types into collections of strings."""

    if isinstance(value, list):
        return [parse_linode_types(elem) for elem in value]

    if isinstance(value, dict):
        return {k: parse_linode_types(elem) for k, elem in value.items()}

    if type(value) in {
        linode_api4.objects.linode.Type,
        linode_api4.objects.linode.Region,
        linode_api4.objects.linode.Image,
        linode_api4.objects.linode.Kernel,
        linode_api4.objects.lke.KubeVersion,
    }:
        return value.id

    if isinstance(value, MappedObject):
        return mapping_to_dict(value)

    return value


def jsonify_node_pool(pool: LKENodePool) -> Dict[str, Any]:
    """Converts an LKENodePool into a JSON-compatible dict"""

    result = pool._raw_json

    result["nodes"] = [jsonify_node_pool_node(node) for node in pool.nodes]

    return result


def jsonify_node_pool_node(node: LKENodePoolNode) -> Dict[str, Any]:
    """Converts an LKENodePoolNode into a JSON-compatible dict"""

    return {
        "id": node.id,
        "instance_id": node.instance_id,
        "status": node.status,
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
        raise Exception("missing fields: {}".format(", ".join(missing_fields)))


def filter_null_values_recursive(obj: Any) -> Any:
    """Recursively removes null values and keys from a structure."""
    if isinstance(obj, dict):
        return {
            k: filter_null_values_recursive(v)
            for k, v in obj.items()
            if v is not None
        }

    if isinstance(obj, (list, set, tuple)):
        return [filter_null_values_recursive(v) for v in obj if v is not None]

    return obj


def construct_api_filter(params: Dict[str, Any]) -> Dict[str, Any]:
    """Constructs a filter string given a list module's params."""

    value_filters = []

    if params.get("filters") is not None:
        for filter_opt in params["filters"]:
            current = []

            for value in filter_opt["values"]:
                current.append({filter_opt["name"]: value})

            value_filters.append(
                {
                    "+or": current,
                }
            )

    result = {"+and": value_filters, "+order": params["order"]}

    if params.get("order_by") is not None:
        result["+order_by"] = params["order_by"]

    return result


def get_all_paginated(
    client: LinodeClient,
    endpoint: str,
    filters: Dict[str, Any],
    num_results=None,
) -> List[Any]:
    """Returns a list of paginated JSON responses for the given API endpoint."""
    result = []
    current_page = 1
    page_size = 100
    num_pages = 1

    if num_results is not None and num_results < page_size:
        # Clamp the page size
        page_size = max(min(num_results, 100), 25)

    while current_page <= num_pages and (
        num_results is None or len(result) < num_results
    ):
        response = client.get(
            endpoint + "?page={}&page_size={}".format(current_page, page_size),
            filters=filters,
        )

        if "data" not in response or "page" not in response:
            raise Exception("Invalid list response")

        result.extend(response["data"])

        if num_results is not None and len(result) >= num_results:
            break

        current_page += 1

    if num_results is not None:
        result = result[:num_results]

    return result


def format_api_error(err: ApiError) -> str:
    """Formats an API error into a readable string"""

    return f"Error from Linode API: [{err.status}] {';'.join(err.errors)}"


def format_generic_error(err: Exception) -> str:
    """Formats a generic error into a readable string"""

    return f"{type(err).__name__}: {str(err)}"


def poll_condition(
    condition_func: Callable[[], bool], step: int, timeout: int
) -> None:
    """Polls for the given condition using the given step and timeout values."""
    # Initial attempt
    if condition_func():
        return

    polling.poll(
        condition_func,
        step=step,
        timeout=timeout,
    )


def safe_find(
    func: Callable[[Tuple[Filter]], List[Any]], *filters: Filter
) -> Any:
    """
    Wraps a resource list function with error handling.
    If no entries are returned, this function returns None rather than
    raising an error.
    """
    try:
        list_results = func(*filters)
        return None if len(list_results) < 1 else list_results[0]
    except Exception as exception:
        raise Exception(f"failed to get resource: {exception}") from exception
