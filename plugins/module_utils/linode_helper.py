"""This module contains helper functions for various Linode modules."""

import traceback
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
    cast,
)

import linode_api4
import polling
from linode_api4 import (
    ApiError,
    JSONObject,
    LinodeClient,
    LKENodePool,
    LKENodePoolNode,
    LKENodePoolTaint,
    MappedObject,
    and_,
)
from linode_api4.objects.filtering import (
    Filter,
    FilterableAttribute,
    FilterableMetaclass,
)
from linode_api4.polling import TimeoutContext


def dict_select_spec(target: dict, spec: dict) -> dict:
    """Returns a new dictionary that only selects the keys from target that are specified in spec"""

    return {key: target.get(key) for key in spec.keys()}


def dict_select_matching(d_1: dict, d_2: dict) -> Tuple[dict, dict]:
    """Returns copies of the given dictionaries with all non-shared keys removed"""

    new_d1 = {key: d_1.get(key) for key in d_2.keys() if key in d_1.keys()}
    new_d2 = {key: d_2.get(key) for key in d_1.keys() if key in d_2.keys()}

    return new_d1, new_d2


def dict_select_matching_recursive(
    *dicts: Dict[str, Any]
) -> Tuple[Dict[str, Any], ...]:
    """Returns copies of the given dictionaries with all non-shared keys removed"""

    result = tuple({} for _ in range(len(dicts)))

    mutual_keys = dicts[0].keys()
    for d in dicts[1:]:
        mutual_keys &= d.keys()

    for key in mutual_keys:
        # Matching key handler
        dict_values = tuple(d.get(key) for d in dicts)

        if all(isinstance(v, dict) for v in dict_values):
            dict_values = dict_select_matching_recursive(*dict_values)
        elif all(isinstance(v, list) for v in dict_values):
            list_values = [[] for _ in range(len(dict_values))]
            longest_list_length = max(len(v) for v in dict_values)

            for list_index in range(longest_list_length):
                # Aggregate a list of (dict_index, dict_value) pairs
                # for dicts with entries for list_index.
                #
                # Pairing is necessary to preserve the index when writing back
                # to the result below.
                relevant_dict_value_pairs = [
                    (i, dict_value[list_index])
                    for i, dict_value in enumerate(dict_values)
                    if list_index < len(dict_value)
                ]

                # We only want to compare entries of dicts with other entries of the same index
                entry_match_result = dict_select_matching_recursive(
                    *[dict_value for _, dict_value in relevant_dict_value_pairs]
                )

                for result_index, (dict_index, _) in enumerate(
                    relevant_dict_value_pairs
                ):
                    # Append an entry to the dict value's corresponding list
                    list_values[dict_index].append(
                        entry_match_result[result_index]
                    )

            dict_values = list_values

        for i, value in enumerate(dict_values):
            result[i][key] = value

    return result


def filter_null_values(input_dict: dict) -> dict:
    """Returns a copy of the given dict with all keys containing null values removed"""
    return {
        key: value for key, value in input_dict.items() if value is not None
    }


def drop_empty_strings(value: Union[dict], recursive=False) -> any:
    """Returns a copy of the given dict with all keys containing null and empty values removed"""

    if isinstance(value, dict):
        result = {}

        for key, item in value.items():
            if item is None or item == "":
                continue

            if recursive:
                result[key] = drop_empty_strings(item, recursive=recursive)
            else:
                result[key] = item

        return result

    return value


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
    obj: linode_api4.Base,
    params: dict,
    mutable_fields: set,
    register_func: Callable,
    ignore_keys: Set[str] = None,
    match_recursive: bool = False,
    dry_run: bool = False,
    nullable_keys: set[str] = None,
    diff_overrides: Dict[str, Callable[[str, Any, Any], bool]] = None,
) -> Set[str]:
    """Handles updates for a linode_api4 object"""

    match_func = (
        dict_select_matching_recursive
        if match_recursive
        else dict_select_matching
    )

    ignore_keys = ignore_keys or set()
    nullable_keys = nullable_keys or set()
    diff_overrides = diff_overrides or {}

    obj._api_get()

    # We need the type to access property metadata
    property_metadata = type(obj).properties

    def _diff_default(_key: str, _old_value: Any, _new_value: Any) -> bool:
        """
        Default diff function for handle_updates.
        """

        if isinstance(_new_value, dict) and isinstance(_old_value, dict):
            # If this field is a dict, we only want to compare values that are
            # specified by the user
            _old_value, _new_value = match_func(
                filter_null_values_recursive(_old_value),
                filter_null_values_recursive(_new_value),
            )

            return _new_value != _old_value

        # We should convert properties to sets
        # if they are annotated as unordered in the
        # Python SDK.
        if (
            property_metadata is not None
            and property_metadata.get(_key) is not None
            and property_metadata.get(_key).unordered
        ):
            return set(_old_value) != set(_new_value)

        return _new_value != _old_value

    # Update mutable values
    params = filter_null_values(params)

    # Populate excluded nullable keys with None
    for key in nullable_keys:
        if key not in params:
            params[key] = None

    put_request = {}
    result = set()

    for key, new_value in params.items():
        if (
            key not in property_metadata
            or not hasattr(obj, key)
            or key in ignore_keys
        ):
            continue

        old_value = parse_linode_types(getattr(obj, key))

        if diff_overrides.get(key, _diff_default)(key, old_value, new_value):
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

    if len(put_request.keys()) > 0 and not dry_run:
        obj._client.put(type(obj).api_endpoint, model=obj, data=put_request)

    return result


def parse_linode_types(value: Any) -> Any:
    """Helper function for handle_updates.
    Parses Linode Object types into collections of strings."""

    if isinstance(value, list):
        return [parse_linode_types(elem) for elem in value]

    if isinstance(value, dict):
        return {k: parse_linode_types(elem) for k, elem in value.items()}

    if issubclass(type(value), JSONObject):
        return parse_linode_types(value.dict)

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
    result["taints"] = [jsonify_node_pool_taint(taint) for taint in pool.taints]

    return result


def jsonify_node_pool_node(node: LKENodePoolNode) -> Dict[str, Any]:
    """Converts an LKENodePoolNode into a JSON-compatible dict"""

    return {
        "id": node.id,
        "instance_id": node.instance_id,
        "status": node.status,
    }


def jsonify_node_pool_taint(taint: LKENodePoolTaint) -> Dict[str, Any]:
    """Converts an LKENodePoolTaint into a JSON-compatible dict"""

    return {
        "key": taint.key,
        "value": taint.value,
        "effect": taint.effect,
    }


def validate_required(required_fields: Set[str], params: Dict[str, Any]):
    """Returns whether the given parameters contain all of the required fields specified."""

    has_missing_field = False
    missing_fields = []

    for required_field in required_fields:
        if required_field not in params:
            missing_fields.append(required_field)
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
    num_pages: Optional[int] = None

    if num_results is not None and num_results < page_size:
        # Clamp the page size
        page_size = max(min(num_results, 100), 25)

    while (num_pages is None or current_page <= num_pages) and (
        num_results is None or len(result) < num_results
    ):
        response = client.get(
            endpoint + "?page={}&page_size={}".format(current_page, page_size),
            filters=filters,
        )

        if "data" not in response or "page" not in response:
            raise Exception("Invalid list response")

        # We only want to set num_pages once to avoid undefined behavior
        # when the number of pages changes mid-aggregation
        num_pages = num_pages or response["pages"]

        result.extend(response["data"])

        if num_results is not None and len(result) >= num_results:
            break

        current_page += 1

    if num_results is not None:
        result = result[:num_results]

    return result


def format_generic_error(exc: Exception, verbosity: int = 0) -> str:
    """Formats a generic error into a readable string"""

    if verbosity > 0:
        return "\n".join(traceback.format_exception(exc))

    return "\n".join(traceback.format_exception_only(exc))


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
    func: Callable[[Tuple[Filter]], List[Any]],
    *filters: Any,
    raise_not_found=False,
) -> Any:
    """
    Wraps a resource list function with error handling.
    If no entries are returned, this function returns None rather than
    raising an error.
    """
    try:
        list_results = func(*filters)
        return list_results[0]
    except IndexError:
        if raise_not_found:
            raise ValueError("No matching resource found.") from IndexError

        return None
    except Exception as exception:
        raise Exception(f"failed to get resource: {exception}") from exception


APIModelT = TypeVar("APIModelT", bound=linode_api4.Base)


@dataclass
class ReconcileSubEntityOperationsResult(Generic[APIModelT]):
    """
    Contains the actions necessary to bring a collection of sub-entities
    up to parity with a set of user-provided params.
    """

    to_create: List[Dict[str, Any]] = field(default_factory=list)
    to_diff: List[Tuple[APIModelT, Dict[str, Any]]] = field(
        default_factory=list
    )
    to_delete: List[APIModelT] = field(default_factory=list)


def reconcile_sub_entity_operations(
    local_entities: List[Dict[str, Any]],
    remote_entities: List[APIModelT],
    entity_matches_param: Callable[[APIModelT, Dict[str, Any]], bool],
) -> ReconcileSubEntityOperationsResult:
    """
    Reconciles the necessary create, update, and delete operations to bring the
    given entities up to parity with the given user-configured entities.
    """
    result = ReconcileSubEntityOperationsResult()
    unhandled_remote_entities = {
        entity.id: entity for entity in remote_entities
    }

    for local_entity in local_entities:
        remote_entity = next(
            (
                v
                for v in unhandled_remote_entities.values()
                if entity_matches_param(v, local_entity)
            ),
            None,
        )

        if remote_entity is None:
            result.to_create.append(local_entity)
            continue

        del unhandled_remote_entities[remote_entity.id]
        result.to_diff.append((remote_entity, local_entity))

    for remote_entity in unhandled_remote_entities.values():
        result.to_delete.append(remote_entity)

    return result


def normalize_params_recursive(
    local_data: Dict[str, Any],
    remote_data: Union[linode_api4.JSONObject, linode_api4.Base],
    normalization_handlers: Dict[Tuple[str, ...], Callable[[Any, Any], Any]],
) -> Dict[str, Any]:
    """
    Modifies the given local data to match the given remote data,
    running the given normalization handlers for each path.
    """

    def __inner(
        local_entry: Any,
        remote_entry: Any,
        current_path: Tuple[str, ...],
    ):
        if local_entry is None or remote_entry is None:
            return local_entry

        if isinstance(local_entry, dict):
            # Recurse through each key in the local entry dict
            for key, local_value in local_entry.items():
                local_entry[key] = __inner(
                    local_value,
                    getattr(remote_entry, key, None),
                    current_path + tuple([key]),
                )

        elif isinstance(local_entry, list):
            # Recurse through pairs of local and remote list entries
            for index, (local_value, remote_value) in enumerate(
                zip(local_entry, remote_entry)
            ):
                # NOTE: We don't extend the path here since indices aren't supported
                # in normalization handler paths.
                local_entry[index] = __inner(
                    local_value, remote_value, current_path
                )

        elif current_path in normalization_handlers:
            # This field has a specified normalization handler
            return normalization_handlers[current_path](
                local_entry, remote_entry
            )

        # Nothing to change
        return local_entry

    return __inner(local_data, remote_data, tuple())


def pop_and_compare_optional_attribute(
    local_parent: Dict[str, Any],
    remote_parent: Dict[str, Any],
    key: str,
    compare: Optional[Callable[[Any, Any], bool]] = None,
) -> bool:
    """
    Returns whether the given key for the local and remote dicts are equivalent,
    ignoring unspecified local values.

    NOTE: This helper pops the keys from their respective dicts.
    """

    if key not in local_parent:
        return True

    local_value = local_parent.pop(key, None)
    remote_value = remote_parent.pop(key, None)

    if compare is not None:
        return compare(local_value, remote_value)

    if isinstance(local_value, dict) and isinstance(remote_value, dict):
        return matching_keys_eq(local_value, remote_value)

    return local_value == remote_value


def matching_keys_eq(
    a: Dict[str, Any],
    b: Dict[str, Any],
):
    """
    Compares values for matching keys in two dicts.
    """

    a, b = dict_select_matching(a, b)
    return b == a


def retry_on_response_status(
    timeout_ctx: TimeoutContext, func: Callable[[], None], *statuses: int
):
    """
    Retries a given function if it raises an ApiError with specific response statuses.
    """

    def __attempt_delete() -> bool:
        try:
            func()
        except ApiError as err:
            if err.status in statuses:
                return False

            raise err

        return True

    poll_condition(
        __attempt_delete,
        step=4,
        timeout=timeout_ctx.seconds_remaining,
    )
