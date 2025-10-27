"""
Contains the Linode interface logic for the linode.cloud.instance module.
"""

import copy
from typing import Any, Dict, Optional, Set

import linode_api4
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values_recursive,
    handle_updates,
    normalize_params_recursive,
    reconcile_sub_entity_operations,
)
from ansible_collections.linode.cloud.plugins.module_utils.modules.instance.util import (
    resolve_terminal_status,
)
from ansible_specdoc.objects import FieldType, SpecField
from linode_api4 import Instance, InterfaceGeneration, LinodeInterface

SPEC_INTERFACE_DEFAULT_ROUTE = {
    "ipv4": SpecField(
        type=FieldType.bool,
        editable=True,
        description=[
            "If set to true, the interface is used for the IPv4 default_route.",
            "Only one interface per Linode can be set as the IPv4 default route.",
        ],
    ),
    "ipv6": SpecField(
        type=FieldType.bool,
        editable=True,
        description=[
            "If set to true, the interface is used for the IPv6 default_route.",
            "Only one interface per Linode can be set as the IPv6 default route.",
        ],
    ),
}


SPEC_INTERFACE_PUBLIC = {
    "ipv4": SpecField(
        type=FieldType.dict,
        editable=True,
        description=[
            "IPv4 address settings for this public interface.",
            "If omitted, a public IPv4 address is automatically allocated.",
        ],
        suboptions={
            "addresses": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                editable=True,
                description=[
                    "List of IPv4 addresses to assign to this interface."
                    "Setting to auto allocates a public IPv4 address."
                ],
                suboptions={
                    "address": SpecField(
                        type=FieldType.string,
                        editable=True,
                        description=[
                            "The public IPv4 address to assign to this interface."
                        ],
                        default="auto",
                    ),
                    "primary": SpecField(
                        type=FieldType.bool,
                        editable=True,
                        description=[
                            "Configures the source address for routes within the Linode "
                            + "on the corresponding network interface."
                        ],
                        default=False,
                    ),
                },
            )
        },
    ),
    "ipv6": SpecField(
        type=FieldType.dict,
        editable=True,
        description=[
            "IPv6 address ranges to assign to this interface.",
            "If omitted, no ranges are assigned.",
        ],
        suboptions={
            "ranges": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                editable=True,
                description=[
                    "IPv6 address ranges to assign to this interface."
                ],
                suboptions={
                    "range": SpecField(
                        type=FieldType.string,
                        editable=True,
                        required=True,
                        description=[
                            "Your assigned IPv6 range in CIDR notation (2001:0db8::1/64) "
                            + "or prefix (/64)."
                        ],
                    )
                },
            )
        },
    ),
}


VPC_INTERFACE_VLAN = {
    "vlan_label": SpecField(
        type=FieldType.string,
        description=[
            "The VLAN's unique label."
            "VLAN interfaces on the same Linode must have a unique vlan_label.",
        ],
    ),
    "ipam_address": SpecField(
        type=FieldType.string,
        description=[
            "This VLAN interface's private IPv4 address in classless "
            + "inter-domain routing (CIDR) notation."
        ],
    ),
}

SPEC_INTERFACE_VPC = {
    "subnet_id": SpecField(
        type=FieldType.integer,
        description=[
            "The VPC subnet identifier for this interface."
            "Your subnet’s VPC must be in the same data center (region) as the Linode."
        ],
    ),
    "ipv4": SpecField(
        type=FieldType.dict,
        editable=True,
        description=[
            "Interfaces can be configured with IPv4 addresses or ranges"
        ],
        suboptions={
            "addresses": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                editable=True,
                suboptions={
                    "address": SpecField(
                        type=FieldType.string,
                        default="auto",
                        editable=True,
                        description=[
                            "Specifies which IPv4 address to use in the VPC subnet."
                        ],
                    ),
                    "nat_1_1_address": SpecField(
                        type=FieldType.string,
                        editable=True,
                        description=[
                            "The 1:1 NAT IPv4 address used to associate a public IPv4 address "
                            "with the interface's VPC subnet IPv4 address."
                        ],
                    ),
                    "primary": SpecField(
                        type=FieldType.bool,
                        editable=True,
                        description=[
                            "This IPv4 primary address is used to configure the source address for "
                            "routes within the Linode on the corresponding network interface."
                        ],
                        default=False,
                    ),
                },
            ),
            "ranges": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                description=["A list of VPC IPv4 ranges."],
                suboptions={
                    "range": SpecField(
                        type=FieldType.string,
                        editable=True,
                        description=[
                            "CIDR notation of a range (1.2.3.4/24) or prefix only (/24)."
                        ],
                    )
                },
            ),
        },
    ),
    "ipv6": SpecField(
        type=FieldType.dict,
        editable=True,
        description=[
            "Interfaces can be configured with IPv6 addresses or ranges."
        ],
        suboptions={
            "is_public": SpecField(
                type=FieldType.bool,
                editable=True,
                description=[
                    "Indicates whether the IPv6 configuration on the Linode interface is public."
                ],
            ),
            "slaac": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                editable=True,
                description=["Defines IPv6 SLAAC address ranges."],
                suboptions={
                    "range": SpecField(
                        type=FieldType.string,
                        default="auto",
                        editable=True,
                        description=[
                            "The IPv6 network range in CIDR notation."
                        ],
                    ),
                },
            ),
            "ranges": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                description=[
                    "Assigned IPv6 SLAAC address ranges, calculated from `addresses` input."
                ],
                suboptions={
                    "range": SpecField(
                        type=FieldType.string,
                        default="auto",
                        editable=True,
                        description=[
                            "The IPv6 network range in CIDR notation."
                        ],
                    )
                },
            ),
        },
    ),
}

SPEC_INTERFACE = linode_instance_linode_interface_spec = {
    "firewall_id": SpecField(
        type=FieldType.integer,
        description=[
            "The enabled firewall to secure a VPC or public interface."
        ],
    ),
    "default_route": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_INTERFACE_DEFAULT_ROUTE,
        editable=True,
        description=[
            "Indicates if the interface serves as the default route "
            + "when multiple interfaces are eligible for this role."
        ],
    ),
    "public": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_INTERFACE_PUBLIC,
        editable=True,
        description=[
            "Defines a Linode public interface.",
            "Any other type must either be omitted or set to null.",
        ],
    ),
    "vlan": SpecField(
        type=FieldType.dict,
        suboptions=VPC_INTERFACE_VLAN,
        editable=True,
        description=[
            "VLAN interface settings.",
            "A Linode can have up to three VLAN interfaces, with a unique vlan_label for each.",
        ],
    ),
    "vpc": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_INTERFACE_VPC,
        editable=True,
        description=[
            "VPC interface settings.",
            "A Linode can have one VPC interface.",
            "The maximum number of interfaces allowed on a Linode is three.",
        ],
    ),
}


def __passthrough_implicit_address(
    local: Optional[str], remote: Optional[str]
) -> Optional[str]:
    """
    Sample: auto -> 10.0.0.5
    """

    return local if local != "auto" else remote


def __passthrough_implicit_range(
    local: Optional[str], remote: Optional[str]
) -> Optional[str]:
    """
    Sample: /24 -> 2001:db8:85a3::8a2e:370:7334/24
    """
    return (
        remote
        if local is not None
        and (local == "auto" or len(local.split("/")[0].strip()) < 1)
        else local
    )


__interface_normalization_handlers = {
    ("public", "ipv4", "addresses", "address"): __passthrough_implicit_address,
    ("public", "ipv6", "ranges", "range"): __passthrough_implicit_range,
    ("vpc", "ipv4", "addresses", "address"): __passthrough_implicit_address,
    (
        "vpc",
        "ipv4",
        "addresses",
        "nat_1_1_address",
    ): __passthrough_implicit_address,
    ("vpc", "ipv4", "ranges", "range"): __passthrough_implicit_range,
    ("vpc", "ipv6", "ranges", "range"): __passthrough_implicit_range,
    ("vpc", "ipv6", "slaac", "range"): __passthrough_implicit_range,
}

INTERFACE_TYPE_KEYS = ["public", "vlan", "vpc"]


def interface_param_matches(
    remote: linode_api4.LinodeInterface, local: Dict[str, Any]
) -> bool:
    """
    Returns whether the given remote and local interface match
    for the purposes of diffing.
    """

    return {v: local.get(v) is not None for v in INTERFACE_TYPE_KEYS} == {
        v: getattr(remote, v) is not None for v in INTERFACE_TYPE_KEYS
    }


def __update_interface(
    module: "LinodeInstance",
    remote: LinodeInterface,
    local: Dict[str, Any],
    dry_run: bool = False,
) -> Set[str]:
    """
    Updates the given interface using the given params.
    """

    if "firewall_id" in local:
        remote_firewall_id = next(
            (v.id for v in remote.firewalls() if v is not None), None
        )

        if remote_firewall_id != local["firewall_id"]:
            raise Exception(
                f"{remote}: firewall_id cannot be updated on an existing interface"
            )

    # Normalize the interface, passing through the remote values
    # if using auto or prefix-only values.
    local_normalized = normalize_params_recursive(
        copy.deepcopy(local),
        remote,
        normalization_handlers=__interface_normalization_handlers,
    )

    return handle_updates(
        remote,
        filter_null_values_recursive(local_normalized),
        {"default_route", "public", "vlan", "vpc"},
        register_func=module.register_action,
        match_recursive=True,
        dry_run=dry_run,
    )


def update_linode_interfaces(
    module: "LinodeInstance",
    instance: Instance,
) -> None:
    """
    Updates the interfaces for the current Linode Instance,
    creating, deleting, and updating interfaces as needed.
    """

    if instance.interface_generation != InterfaceGeneration.LINODE:
        return

    local_interfaces = module.module.params.get("linode_interfaces", None)
    if local_interfaces is None:
        return

    operations = reconcile_sub_entity_operations(
        local_interfaces, instance.linode_interfaces, interface_param_matches
    )

    needs_updates = (
        any(
            len(__update_interface(module, remote, local, dry_run=True)) > 0
            for remote, local in operations.to_diff
        )
        or len(operations.to_create) > 0
        or len(operations.to_delete) > 0
    )

    if not needs_updates:
        return

    allow_implicit_reboots = module.module.params.get(
        "allow_implicit_reboots", False
    )

    module.client.polling.wait_for_entity_free(
        "linode",
        instance.id,
        timeout=module._timeout_ctx.seconds_remaining,
    )
    instance.invalidate()

    # Shutdown the instance if necessary
    if resolve_terminal_status(instance) == "running":
        if not allow_implicit_reboots:
            raise ValueError(
                "Cannot update Linode interfaces on a running Linode. "
                "Set allow_implicit_reboots to true to allow this Linode to be implicitly "
                "rebooted."
            )

        module._restore_boot_status = True

        shutdown_poller = module.client.polling.event_poller_create(
            "linode", "linode_shutdown", instance.id
        )

        module.register_action("Powered off Linode for interface updates")
        instance.shutdown()

        shutdown_poller.wait_for_next_event_finished(
            timeout=module._timeout_ctx.seconds_remaining,
        )

    for local in operations.to_create:
        new_interface = instance.interface_create(
            **local,
        )
        module.register_action(f"Created Linode interface {new_interface.id}")

    for remote, local in operations.to_diff:
        __update_interface(module, remote, local, dry_run=False)
        remote._api_get()

    for remote in operations.to_delete:
        module.register_action(f"Deleted Linode interface {remote.id}")
        remote.delete()
