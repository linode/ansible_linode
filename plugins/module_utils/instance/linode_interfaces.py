import copy
from typing import Any, Callable, Dict, List, Optional, Set, Union

import linode_api4
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    handle_updates,
)
from linode_api4 import Instance, LinodeInterface


def __ip_is_explicit(value: Optional[str]) -> bool:
    """
    Returns whether the given IP address is explicitly set or is implicit (auto, /PREFIX).
    """

    if value is None:
        return False

    value = value.strip()
    return value != "auto" and len(value.split("/")[0].strip()) < 1


def __normalize_lists(
    local_list: List[Dict[str, Any]],
    remote_list: List[Union[linode_api4.JSONObject, linode_api4.Base]],
    passthrough_keys: Set[str],
    is_explicit: Callable[[str], bool] = __ip_is_explicit,
) -> List[Dict[str, Any]]:
    result = copy.deepcopy(local_list)

    for i, (local_entry, remote_entry) in enumerate(
        zip(local_list, remote_list)
    ):
        for passthrough_key in passthrough_keys:
            if passthrough_key not in local_entry:
                continue

            if is_explicit(passthrough_key):
                # Pass-through the explicit value
                continue

            result[i][passthrough_key] = getattr(remote_entry, passthrough_key)

    result.sort(
        key=lambda entry: tuple(entry.get(key) for key in passthrough_keys)
    )

    return result


def __normalize_local_linode_interface_public(
    local_public: Dict[str, Any], remote_public: LinodeInterface
) -> Dict[str, Any]:
    result = copy.deepcopy(local_public)

    def __normalize_ipv4() -> Dict[str, Any]:
        local_ipv4 = local_public.get("ipv4")
        remote_ipv4 = remote_public.ipv4

        result = copy.deepcopy(local_ipv4)

        if local_ipv4 is None or remote_ipv4 is None:
            return result

        result["addresses"] = __normalize_lists(
            local_ipv4.get("addresses"),
            remote_ipv4.addresses,
            {"address"},
        )

        return result

    def __normalize_ipv6() -> Dict[str, Any]:
        local_ipv6 = local_public.get("ipv6")
        remote_ipv6 = remote_public.ipv6

        result = copy.deepcopy(local_ipv6)

        if local_ipv6 is None or remote_ipv6 is None:
            return result

        result["ranges"] = __normalize_lists(
            local_ipv6.get("ranges"),
            remote_ipv6.ranges,
            {"range"},
        )

        return result

    result["ipv4"] = __normalize_ipv4()
    result["ipv6"] = __normalize_ipv6()

    return result


def __normalize_local_linode_interface_vpc(
    local_vpc: Dict[str, Any], remote_vpc: LinodeInterface
) -> Dict[str, Any]:
    result = copy.deepcopy(local_vpc)

    def __normalize_ipv4() -> Dict[str, Any]:
        local_ipv4 = local_vpc.get("ipv4")
        remote_ipv4 = remote_vpc.ipv4

        result = copy.deepcopy(local_ipv4)

        if local_ipv4 is None or remote_ipv4 is None:
            return result

        result["addresses"] = __normalize_lists(
            local_ipv4.get("addresses"),
            remote_ipv4.addresses,
            {"address", "nat_1_1_address"},
        )

        result["ranges"] = __normalize_lists(
            local_ipv4.get("ranges"),
            remote_ipv4.ranges,
            {"range"},
        )

        return result

    result["ipv4"] = __normalize_ipv4()

    return result


def __normalize_local_linode_interface(
    local_interface: Dict[str, Any], remote_interface: LinodeInterface
) -> Dict[str, Any]:
    """
    Normalizes the given param interface to the remote interface
    for direct comparison.
    """
    result = copy.deepcopy(local_interface)

    # `public` normalization
    local_public = local_interface.get("public")
    remote_public = remote_interface.public
    if local_public is not None and remote_public is not None:
        result["public"] = __normalize_local_linode_interface_public(
            local_public, remote_public
        )

    # `vpc` normalization
    local_vpc = local_interface.get("vpc")
    remote_vpc = remote_interface.vpc
    if local_vpc is not None and remote_vpc is not None:
        result["vpc"] = __normalize_local_linode_interface_vpc(
            local_vpc, remote_vpc
        )

    return result


def __find_matching_interface(
    local_interface: Dict[str, Any],
    remote_interfaces: List[LinodeInterface],
    exclude_ids: Set[int],
) -> Optional[LinodeInterface]:
    """
    Returns a single entry from remote_interfaces that roughly matches
    the given local_interface.

    Entries of remote_interfaces with ids in the exclude_ids set will be
    ignored.
    """
    for remote_interface in remote_interfaces:
        if remote_interface.id in exclude_ids:
            continue

        for field in ["public", "vlan", "vpc"]:
            # If the interface types match, assume this is a match
            if (
                local_interface.get(field) is None
                or getattr(remote_interface, field) is None
            ):
                continue

            return remote_interface

    return None


def update_linode_interfaces(
    module: LinodeModuleBase,
    instance: Instance,
) -> None:
    """
    Updates the interfaces for the current Linode Instance,
    creating, deleting, and updating interfaces as needed.
    """

    # TODO(Linode Interfaces): allow_implicit_reboots logic

    local_interfaces = module.module.params.get("linode_interfaces", None)
    if local_interfaces is None:
        return

    remote_interfaces = instance.interfaces

    # Reconcile create/read/delete operations
    handled_interface_ids = set()

    for local_interface in local_interfaces:
        related_interface = __find_matching_interface(
            local_interface, remote_interfaces, handled_interface_ids
        )

        if related_interface is None:
            # Create an interface
            new_interface = instance.interface_create(
                **local_interface,
            )
            handled_interface_ids.add(new_interface.id)
            module.register_action(f"Created interface {new_interface.id}")
            continue

        # Update an interface
        normalized_local_interface = __normalize_local_linode_interface(
            local_interface, related_interface
        )

        handle_updates(
            related_interface,
            normalized_local_interface,
            {"default_route", "public", "vlan", "vpc"},
            register_func=module.register_action,
            ignore_keys={"firewall_id"},
        )

        handled_interface_ids.add(related_interface.id)

        related_interface._api_get()

    # Delete remaining interface
    for remote_interface in remote_interfaces:
        if remote_interface.id in handled_interface_ids:
            continue

        module.register_action(f"Deleted interface {remote_interface.id}")
        remote_interface.delete()

    return
