#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the functionality for NAT Gateways."""

import time
from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.natgateway as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    handle_updates,
    mapping_to_dict,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ApiError, NATGateway

SPEC = {
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    "id": SpecField(
        type=FieldType.integer,
        description=["The ID of the NAT Gateway."],
    ),
    "label": SpecField(
        type=FieldType.string,
        description=[
            "The label of the NAT Gateway. "
            "This field can only contain ASCII letters, digits and dashes."
        ],
        editable=True,
    ),
    "addresses": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        description=[
            "The list of IP addresses assigned to the NAT Gateway. "
            "Addresses cannot be modified when the NAT Gateway uses autoscaling, "
            "as the API manages them in that case."
        ],
        suboptions={
            "address": SpecField(
                type=FieldType.string,
                required=True,
                description=["The IPv4 address."],
            )
        },
        editable=True,
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The region that the NAT Gateway is in."],
    ),
    "default_ports_per_interface": SpecField(
        type=FieldType.integer,
        description=["The default number of ports per interface."],
    ),
    "use_autoscaling": SpecField(
        type=FieldType.bool,
        description=[
            "Whether or not to use autoscaling. "
            "This field is set during creation and cannot be changed after creation. "
            "It is ignored for existing NAT Gateways."
        ],
    ),
    "vpc_subnet_id": SpecField(
        type=FieldType.integer,
        description=[
            "The ID of the VPC subnet that the NAT Gateway is in. "
            "This field is set during creation and cannot be changed after creation."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Manage a NAT Gateway.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "natgateway": SpecReturnValue(
            description="The returned NAT Gateway.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-natgateway",
            type=FieldType.dict,
            sample=docs.result_natgateway_samples,
        ),
        "addresses": SpecReturnValue(
            description="The list of IP addresses assigned to the NAT Gateway.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-natgateway-addresses",
            type=FieldType.list,
            sample=docs.result_addresses_samples,
        ),
    },
)

CREATE_FIELDS = {
    "label",
    "region",
    "addresses",
    "use_autoscaling",
    "default_ports_per_interface",
    "vpc_subnet_id",
}

MUTABLE_FIELDS = {"label"}

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying NAT Gateways"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "natgateway": None,
            "addresses": None,
        }

        self._natgateway: Optional[NATGateway] = None
        self._state = "present"

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
        )

    def _get_natgateway_by_label(self, label: str) -> Optional[NATGateway]:
        attempt = 0
        retries = 5
        retry_delay = 3

        while attempt < retries:
            try:
                return self.client.networking.natgateways(
                    NATGateway.label == label
                )[0]
            except IndexError:
                attempt += 1
                if attempt < retries:
                    time.sleep(retry_delay)
                else:
                    return None
            except Exception as exception:
                return self.fail(
                    msg="failed to get NAT Gateway {0}: {1}".format(
                        label, exception
                    )
                )
        return None

    def _get_natgateway_by_id(self, natgateway_id: int) -> Optional[NATGateway]:
        try:
            return self.client.load(NATGateway, natgateway_id)
        except ApiError as exception:
            if exception.status == 404:
                return None
            return self.fail(
                msg="failed to get NAT Gateway {0}: {1}".format(
                    natgateway_id, exception
                )
            )
        except Exception as exception:
            return self.fail(
                msg="failed to get NAT Gateway {0}: {1}".format(
                    natgateway_id, exception
                )
            )

    def _create_natgateway(self) -> Optional[NATGateway]:
        """Creates a NAT Gateway with the given kwargs"""

        params = filter_null_values(
            {
                "label": self.module.params.get("label"),
                "region": self.module.params.get("region"),
                "addresses": self.module.params.get("addresses"),
                "use_autoscaling": self.module.params.get("use_autoscaling"),
                "default_ports_per_interface": self.module.params.get(
                    "default_ports_per_interface"
                ),
                "vpc_subnet_id": self.module.params.get("vpc_subnet_id"),
            }
        )

        try:
            return self.client.networking.natgateway_create(**params)
        except Exception as exception:
            return self.fail(msg=f"failed to create NAT Gateway: {exception}")

    def _update_natgateway(self) -> None:
        """Handles all update functionality for the current NAT Gateway"""

        # Filter out addresses to handle separately
        params = filter_null_values(self.module.params)
        params.pop("addresses", None)

        # Creation-only fields are excluded from the generic update check;
        # only reject changes that can be detected against the current gateway.
        vpc_subnet_id = params.pop("vpc_subnet_id", None)

        # use_autoscaling is not returned by the API, so it cannot be compared
        # and is ignored for existing gateways.
        params.pop("use_autoscaling", None)

        if vpc_subnet_id is not None:
            current_subnet = self._natgateway.vpc_subnet
            current_subnet_id = current_subnet.id if current_subnet else None
            if current_subnet_id != vpc_subnet_id:
                self.fail(
                    msg="vpc_subnet_id cannot be changed after gateway creation "
                    f"(current: {current_subnet_id}, requested: {vpc_subnet_id})"
                )

        # Handle label and other updates
        handle_updates(
            self._natgateway,
            params,
            MUTABLE_FIELDS,
            self.register_action,
        )

        # Handle address updates separately
        spec_addresses = self.module.params.get("addresses")
        if spec_addresses is not None:
            self._update_addresses(spec_addresses)

    def _get_natgateway_addresses(self) -> list:
        """Get current address assignments for this NAT Gateway as a list"""
        try:
            return [
                mapping_to_dict(addr)
                for addr in self._natgateway.address_assignments()
            ]
        except Exception as exception:
            self.fail(
                msg="failed to get NAT Gateway addresses: {0}".format(exception)
            )
            return []

    def _add_address(self, address: str) -> None:
        self._natgateway.address_assignment_create(address)
        self.register_action("Added address {}".format(address))

    def _delete_address(self, address: str) -> None:
        self._natgateway.address_assignment_delete(address)
        self.register_action("Deleted address {}".format(address))

    def _check_address_capacity(
        self, current: set, to_add: set, to_remove: set
    ) -> int:
        """
        Validates the desired address count against the account's per-gateway
        limit and returns how many removals must happen before additions.
        """
        try:
            settings = self.client.networking.natgateway_settings()
            limit = settings.maximum_reserved_addresses_per_natgateway
        except Exception as exception:
            self.fail(msg=f"failed to get NAT Gateway settings: {exception}")
            return 0

        desired_count = len(current) - len(to_remove) + len(to_add)
        if desired_count > limit:
            self.fail(
                msg=f"{desired_count} addresses requested, but this account "
                f"allows at most {limit} per NAT Gateway"
            )
            return 0

        overflow = len(current) + len(to_add) - limit
        if overflow <= 0:
            return 0

        self.warn(
            "Adding addresses before removing old ones would exceed the limit "
            f"of {limit} per NAT Gateway; removing {overflow} address(es) "
            "first. The gateway will briefly have reduced egress capacity."
        )
        return overflow

    def _rollback_addresses(self, added: list, removed: list) -> None:
        """Best-effort restore of the original address set."""
        for address in added:
            try:
                self._delete_address(address)
            except Exception:
                # Best-effort rollback; ignore deletion failures to ensure
                # the original failure is reported to the user
                pass

        for address in removed:
            try:
                self._add_address(address)
            except Exception:
                # Best-effort rollback; ignore re-add failures to ensure
                # the original failure is reported to the user
                pass

    def _update_addresses(self, spec_addresses: list) -> None:
        """Sync addresses to desired state"""
        # Get current addresses from API (single call, converted to JSON list)
        current_addresses_list = self._get_natgateway_addresses()
        current_addresses = {
            addr.get("address") for addr in current_addresses_list
        }

        # Get desired addresses
        desired_addresses = {
            addr.get("address") for addr in (spec_addresses or [])
        }

        # Determine addresses to add and remove
        addresses_to_add = desired_addresses - current_addresses
        addresses_to_remove = current_addresses - desired_addresses

        if not addresses_to_add and not addresses_to_remove:
            return

        early_remove_count = 0
        if addresses_to_add:
            early_remove_count = self._check_address_capacity(
                current_addresses, addresses_to_add, addresses_to_remove
            )

        # Prefer removing addresses that are not in use when freeing slots early
        in_use = {
            addr.get("address")
            for addr in current_addresses_list
            if addr.get("in_use")
        }
        ordered_removals = sorted(
            addresses_to_remove, key=lambda addr: (addr in in_use, addr)
        )
        early_removals = ordered_removals[:early_remove_count]
        late_removals = ordered_removals[early_remove_count:]

        # Free only the slots needed to stay within the per-gateway limit
        removed_addresses = []
        for address in early_removals:
            try:
                self._delete_address(address)
                removed_addresses.append(address)
            except Exception as exception:
                self._rollback_addresses([], removed_addresses)
                self.fail(
                    msg="failed to delete address {0}: {1}".format(
                        address, exception
                    )
                )

        # Add new addresses before removing the remaining old ones to avoid
        # leaving the gateway without egress
        added_addresses = []
        for address in sorted(addresses_to_add):
            try:
                self._add_address(address)
                added_addresses.append(address)
            except Exception as exception:
                self._rollback_addresses(added_addresses, removed_addresses)
                self.fail(
                    msg="failed to add address {0}: {1}".format(
                        address, exception
                    )
                )

        # Remove addresses not in desired state (only after new addresses are confirmed)
        for address in late_removals:
            try:
                self._delete_address(address)
            except Exception as exception:
                self.fail(
                    msg="failed to delete address {0}: {1}".format(
                        address, exception
                    )
                )

    def _handle_present(self) -> None:
        """Updates the NAT Gateway defined in kwargs"""

        natgateway_id = self.module.params.get("id")
        natgateway_label = self.module.params.get("label")

        # Get existing NAT Gateway by id or label
        if natgateway_id is not None:
            self._natgateway = self._get_natgateway_by_id(natgateway_id)
        elif natgateway_label is not None:
            self._natgateway = self._get_natgateway_by_label(natgateway_label)

        # Create NAT Gateway if doesn't exist
        if self._natgateway is None:
            if natgateway_id is not None:
                self.fail("NAT Gateway {} not found".format(natgateway_id))
                return
            if natgateway_label is None:
                self.fail("label is required to create a NAT Gateway")
                return
            self._natgateway = self._create_natgateway()
            self.register_action(
                "Created NAT Gateway {}".format(natgateway_label)
            )
        else:
            self._update_natgateway()

        if self._natgateway is None:
            self.fail("failed to create NAT Gateway")
            return

        self._natgateway._api_get()

        self.results["natgateway"] = self._natgateway._raw_json
        self.results["addresses"] = self._get_natgateway_addresses()

    def _handle_absent(self) -> None:
        """Handles deletion of NAT Gateway for the absent state"""

        natgateway_id = self.module.params.get("id")
        natgateway_label = self.module.params.get("label")

        # Get existing NAT Gateway by id or label
        if natgateway_id is not None:
            self._natgateway = self._get_natgateway_by_id(natgateway_id)
        elif natgateway_label is not None:
            self._natgateway = self._get_natgateway_by_label(natgateway_label)

        if self._natgateway is not None:
            self.results["natgateway"] = self._natgateway._raw_json
            self._natgateway.delete()
            self.register_action(
                "Deleted NAT Gateway {}".format(
                    natgateway_label or natgateway_id
                )
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for NAT Gateway module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode NAT Gateway module"""
    Module()


if __name__ == "__main__":
    main()
