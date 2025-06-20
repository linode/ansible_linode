from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values_recursive,
    handle_updates,
)
from ansible_specdoc.objects import FieldType, SpecField
from linode_api4 import Instance

SPEC_INTERFACES_SETTINGS = {
    "network_helper": SpecField(
        type=FieldType.bool,
        description=[
            "Enables the Network Helper feature.",
            "The default value is determined by the network_helper setting in the account settings.",
            "Power off the Linode before disabling or enabling Network Helper.",
        ],
    ),
    "default_route": SpecField(
        type=FieldType.dict,
        description=[
            "Interfaces used for the IPv4 default_route and IPv6 default_route when "
            "multiple interfaces are eligible for the role."
        ],
        suboptions={
            "ipv4_interface_id": SpecField(
                type=FieldType.integer,
                description=[
                    "The VPC or public interface ID assigned as the IPv4 default_route."
                ],
            ),
            "ipv6_interface_id": SpecField(
                type=FieldType.integer,
                description=[
                    "The VPC or public interface ID assigned as the IPv6 default_route."
                ],
            ),
        },
    ),
}


def update_linode_interfaces_settings(
    module: "LinodeInstance",
    instance: Instance,
) -> None:
    """
    Updates the Linode interfaces settings for the current Linode Instance.
    """

    local = module.module.params.get("linode_interfaces_settings", None)
    remote = instance.interfaces_settings

    if local is None:
        return

    handle_updates(
        remote,
        filter_null_values_recursive(local),
        {"default_route", "network_helper"},
        register_func=module.register_action,
        match_recursive=True,
    )
