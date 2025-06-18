import copy
from typing import Any, Dict, List, Optional, Set

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    handle_updates,
    normalize_params_recursive,
)
from linode_api4 import Instance, LinodeInterface


def __explicit_address(
    local: Optional[str], remote: Optional[str]
) -> Optional[str]:
    return local if local != "auto" else remote


def __explicit_range(
    local: Optional[str], remote: Optional[str]
) -> Optional[str]:
    return (
        remote
        if local is not None and len(local.split("/")[0].strip()) < 1
        else local
    )


__interface_normalization_handlers = {
    ("public", "ipv4", "addresses", "address"): __explicit_address,
    ("public", "ipv6", "ranges", "range"): __explicit_range,
    ("vpc", "ipv4", "addresses", "address"): __explicit_address,
    ("vpc", "ipv4", "addresses", "nat_1_1_address"): __explicit_address,
    ("vpc", "ipv6", "ranges", "range"): __explicit_range,
}


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

        # Update the interface

        # Normalize the interface, passing through the remote values
        # if using auto or prefix-only values.
        normalized_local_interface = normalize_params_recursive(
            copy.deepcopy(local_interface),
            related_interface,
            normalization_handlers=__interface_normalization_handlers,
        )

        handle_updates(
            related_interface,
            normalized_local_interface,
            {"default_route", "public", "vlan", "vpc"},
            register_func=module.register_action,
            # TODO: firewall_id change error or device update logic?
            ignore_keys={"firewall_id"},
        )

        handled_interface_ids.add(related_interface.id)
        related_interface._api_get()

    # Delete the remaining interfaces
    for remote_interface in remote_interfaces:
        if remote_interface.id in handled_interface_ids:
            continue

        module.register_action(f"Deleted interface {remote_interface.id}")
        remote_interface.delete()

    return
