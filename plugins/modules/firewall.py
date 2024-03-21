#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Firewalls."""

from __future__ import absolute_import, division, print_function

import copy
import ipaddress
from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    filter_null_values_recursive,
    mapping_to_dict,
    paginated_list_to_json,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)

try:
    from linode_api4 import Firewall, FirewallDevice
except ImportError:
    # handled in module_utils.linode_common
    pass

linode_firewall_addresses_spec: dict = {
    "ipv4": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=[
            "A list of IPv4 addresses or networks.",
            "Must be in IP/mask format.",
        ],
    ),
    "ipv6": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=[
            "A list of IPv6 addresses or networks.",
            "Must be in IP/mask format.",
        ],
    ),
}

linode_firewall_rule_spec: dict = {
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["The label of this rule."],
    ),
    "action": SpecField(
        type=FieldType.string,
        choices=["ACCEPT", "DROP"],
        required=True,
        description=[
            "Controls whether traffic is accepted or dropped by this rule."
        ],
    ),
    "addresses": SpecField(
        type=FieldType.dict,
        suboptions=linode_firewall_addresses_spec,
        description=["Allowed IPv4 or IPv6 addresses."],
    ),
    "description": SpecField(
        type=FieldType.string, description=["A description for this rule."]
    ),
    "ports": SpecField(
        type=FieldType.string,
        description=[
            "A string representing the port or ports on which traffic will be allowed.",
            "See https://www.linode.com/docs/api/networking/#firewall-create",
        ],
    ),
    "protocol": SpecField(
        type=FieldType.string,
        description=["The type of network traffic to allow."],
    ),
}


linode_firewall_rules_spec: dict = {
    "inbound": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_firewall_rule_spec,
        description=["A list of rules for inbound traffic."],
    ),
    "inbound_policy": SpecField(
        type=FieldType.string,
        description=["The default behavior for inbound traffic."],
    ),
    "outbound": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_firewall_rule_spec,
        description=["A list of rules for outbound traffic."],
    ),
    "outbound_policy": SpecField(
        type=FieldType.string,
        description=["The default behavior for outbound traffic."],
    ),
}

linode_firewall_device_spec: dict = {
    "id": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The unique ID of the device to attach to this Firewall."],
    ),
    "type": SpecField(
        type=FieldType.string,
        default="linode",
        description=["The type of device to be attached to this Firewall."],
    ),
}

linode_firewall_spec: dict = {
    "label": SpecField(
        type=FieldType.string,
        description=["The unique label to give this Firewall."],
    ),
    "devices": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_firewall_device_spec,
        editable=True,
        description=["The devices that are attached to this Firewall."],
    ),
    "rules": SpecField(
        type=FieldType.dict,
        suboptions=linode_firewall_rules_spec,
        editable=True,
        description=[
            "The inbound and outbound access rules to apply to this Firewall."
        ],
    ),
    "status": SpecField(
        type=FieldType.string,
        editable=True,
        description=["The status of this Firewall."],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent", "update"],
        required=True,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode Firewalls."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_firewall_spec,
    examples=docs.specdoc_examples,
    return_values={
        "firewall": SpecReturnValue(
            description="The Firewall description in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/networking/#firewall-view",
            type=FieldType.dict,
            sample=docs.result_firewall_samples,
        ),
        "devices": SpecReturnValue(
            description="A list of Firewall devices JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/networking/#firewall-device-view",
            type=FieldType.list,
            sample=docs.result_devices_samples,
        ),
    },
)

# Fields that can be updated on an existing Firewall
linode_firewall_mutable: List[str] = ["status", "tags"]


class LinodeFirewall(LinodeModuleBase):
    """Module for creating and destroying Linode Firewalls"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec

        self.results: dict = {
            "changed": False,
            "actions": [],
            "firewall": None,
            "devices": None,
        }

        self._firewall: Optional[Firewall] = None

        self._state = "present"

        super().__init__(module_arg_spec=self.module_arg_spec)

    def _get_firewall_by_label(self, label: str) -> Optional[Firewall]:
        try:
            return self.client.networking.firewalls(Firewall.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get firewall {0}: {1}".format(label, exception)
            )

    def _create_firewall(self) -> dict:
        params = self.module.params

        label = params.get("label")
        rules = filter_null_values_recursive(params["rules"])
        tags = params["tags"]
        try:
            result = self.client.networking.firewall_create(
                label, rules=rules, tags=tags
            )
        except Exception as exception:
            self.fail(msg="failed to create firewall: {0}".format(exception))

        return result

    def _create_device(
        self, device_id: int, device_type: str, **spec_args: Any
    ) -> None:
        self._firewall.device_create(device_id, device_type, **spec_args)
        self.register_action(
            "Created device {0} of type {1}".format(device_id, device_type)
        )

    def _delete_device(self, device: FirewallDevice) -> None:
        self.register_action(
            "Deleted device {0} of type {1}".format(
                device.entity.id, device.entity.type
            )
        )
        device.delete()

    def _update_devices(self, spec_devices: list) -> None:
        # Remove devices that are not present in config
        device_map = {}

        for device in self._firewall.devices:
            device_map[device.entity.id] = device

        # Handle creating/keeping existing devices
        for device in spec_devices:
            device_entity_id = device.get("id")
            device_entity_type = device.get("type")

            if device_entity_id in device_map:
                if (
                    device_map[device_entity_id].entity.type
                    == device_entity_type
                ):
                    del device_map[device_entity_id]
                    continue

                # Recreate the device if the fields don't match
                self._delete_device(device_map[device_entity_id])

            self._create_device(device_entity_id, device_entity_type)

        # Delete unused devices
        for device in device_map.values():
            self._delete_device(device)

    @staticmethod
    def _normalize_ips(rules: list) -> list:
        result = []
        for rule in rules:
            item = copy.deepcopy(rule)

            addresses = rule.get("addresses", [])

            if "ipv6" in addresses:
                item["addresses"]["ipv6"] = [
                    str(ipaddress.IPv6Network(v)) for v in addresses["ipv6"]
                ]

            if "ipv4" in addresses:
                item["addresses"]["ipv4"] = [
                    str(ipaddress.IPv4Network(v)) for v in addresses["ipv4"]
                ]

            result.append(item)

        return result

    @staticmethod
    def _amend_rules(remote_rules: list, local_rules: list) -> list:
        # produce a result list in the same order as remote_rules
        # amended by the updates from the local_rules

        local_labeled_rules = {r["label"]: r for r in local_rules}
        result = []
        for remote_rule in remote_rules:
            # copy remote_rule as is if not being updated by local_rules
            if remote_rule["label"] not in local_labeled_rules:
                result.append(remote_rule)
                continue

            # insert all missing fields in local_rule from remote_rule
            local_rule = local_labeled_rules[remote_rule["label"]]
            for field in linode_firewall_rule_spec:
                if field not in local_rule and field in remote_rule:
                    local_rule[field] = remote_rule[field]

            for ip_version in ["ipv6", "ipv4"]:
                if ip_version in local_rule.get("addresses", {}):
                    continue

                remote_addresses = remote_rule.get("addresses", {})
                local_addresses = local_rule.get("addresses", {})
                local_addresses[ip_version] = remote_addresses.get(
                    ip_version, None
                )
                local_rule["addresses"] = local_addresses

            result.append(local_rule)
        return result

    def _update_rules(self, remote_rules: dict, local_rules: dict) -> dict:
        # Amend existing rules with user-supplied rules
        if self._state != "update":
            return local_rules

        # Add new local rules to remote rules if they don't exist
        for direction in ["inbound", "outbound"]:
            rlr = {
                remote_rule["label"]
                for remote_rule in remote_rules.get(direction, {})
            }
            for local_rule in local_rules.get(direction, {}):
                if local_rule["label"] not in rlr:
                    remote_rules[direction].append(local_rule)

        for direction in ["inbound", "outbound"]:
            local_rules[direction] = self._amend_rules(
                remote_rules[direction], local_rules[direction]
            )
        return local_rules

    def _change_rules(self) -> Optional[dict]:
        """Updates remote firewall rules relative to user-supplied new rules,
        and returns whether anything changed."""
        local_rules = filter_null_values_recursive(self.module.params["rules"])
        remote_rules = filter_null_values_recursive(
            mapping_to_dict(self._firewall.rules)
        )

        # user did not specify any rules updates
        if local_rules is None:
            local_rules = {}

        if remote_rules is None:
            remote_rules = {}

        # Normalize IP addresses for all rules
        for direction in ["inbound", "outbound"]:
            if direction in local_rules:
                local_rules[direction] = self._normalize_ips(
                    local_rules[direction]
                )
            else:
                local_rules[direction] = []

            if direction in remote_rules:
                remote_rules[direction] = self._normalize_ips(
                    remote_rules[direction]
                )
            else:
                remote_rules[direction] = []

        # Update local_rules with missing information from remote_rules
        local_rules = self._update_rules(remote_rules, local_rules)

        # Sync policy
        for policy in ["inbound_policy", "outbound_policy"]:
            if policy not in local_rules:
                local_rules[policy] = remote_rules[policy]

        local_rules = filter_null_values_recursive(local_rules)
        remote_rules = filter_null_values_recursive(remote_rules)
        return local_rules if local_rules != remote_rules else None

    def _update_firewall(self) -> None:
        """Handles all update functionality for the current Firewall"""

        # Update mutable values
        should_update = False
        params = filter_null_values(self.module.params)

        for key, new_value in params.items():
            if not hasattr(self._firewall, key):
                continue

            old_value = getattr(self._firewall, key)

            if new_value != old_value:
                if key in linode_firewall_mutable:
                    setattr(self._firewall, key, new_value)
                    self.register_action(
                        'Updated Firewall {0}: "{1}" -> "{2}"'.format(
                            key, old_value, new_value
                        )
                    )

                    should_update = True

        if should_update:
            self._firewall.save()

        changes = self._change_rules()
        if changes:
            self._firewall.update_rules(changes)
            self.register_action("Updated Firewall rules")

        # Update devices
        devices: Optional[List[Any]] = params.get("devices")
        if devices is not None:
            self._update_devices(devices)

    def _handle_present(self) -> None:
        """Updates the Firewall"""
        label = self.module.params.get("label")

        self._firewall = self._get_firewall_by_label(label)

        if self._firewall is None:
            self._firewall = self._create_firewall()
            self.register_action("Created Firewall {0}".format(label))

        self._update_firewall()

        self._firewall._api_get()

        self.results["firewall"] = self._firewall._raw_json
        self.results["devices"] = paginated_list_to_json(self._firewall.devices)

    def _handle_absent(self) -> None:
        """Destroys the Firewall"""
        label = self.module.params.get("label")

        self._firewall = self._get_firewall_by_label(label)

        if self._firewall is not None:
            self.results["firewall"] = self._firewall._raw_json
            self.results["devices"] = paginated_list_to_json(
                self._firewall.devices
            )
            self.register_action("Deleted Firewall {0}".format(label))
            self._firewall.delete()

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Firewall module"""

        self._state = self.module.params.get("state")

        if self._state == "absent":
            self._handle_absent()
        else:
            self._handle_present()
        return self.results


def main() -> None:
    """Constructs and calls the Linode Firewall module"""

    LinodeFirewall()


if __name__ == "__main__":
    main()
