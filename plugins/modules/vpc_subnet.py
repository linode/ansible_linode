#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode VPCs."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet as docs
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
    retry_on_response_status,
    safe_find,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_networking import (
    auto_alloc_ranges_equivalent,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_vpc_shared import (
    should_retry_subnet_delete_400s,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import VPC, VPCSubnet

SPEC = {
    "vpc_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The ID of the parent VPC for this subnet."],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["This VPC's unique label."],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this token."],
    ),
    "ipv4": SpecField(
        type=FieldType.string,
        description=["The IPV4 range for this subnet in CIDR format."],
    ),
    "ipv6": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        description=[
            "The IPv6 ranges of this subnet.",
            "NOTE: IPv6 VPCs may not currently be available to all users.",
        ],
        suboptions={
            "range": SpecField(
                type=FieldType.string,
                description="An existing IPv6 prefix owned by the current account "
                + "or a forward slash (/) followed by a valid prefix length. "
                + "If unspecified, a range with the default prefix will be allocated for this VPC.",
            ),
        },
    ),
}


SPECDOC_META = SpecDocMeta(
    description=[
        "Create, read, and update a Linode VPC Subnet.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "subnet": SpecReturnValue(
            description="The VPC in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpc-subnet",
            type=FieldType.dict,
            sample=docs.result_subnet_samples,
        )
    },
)

CREATE_FIELDS = {"label", "ipv4", "ipv6"}

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode VPCS"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"changed": False, "actions": [], "vpc": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
        )

    def __ipv6_updated(self, subnet: VPCSubnet) -> bool:
        ipv6_arg = self.module.params.get("ipv6")
        if ipv6_arg is None:
            return False

        ipv6_actual = subnet.ipv6 or []

        if len(ipv6_arg) != len(ipv6_actual):
            return True

        for i, entry_arg in enumerate(ipv6_arg):
            range_arg = entry_arg.get("range")

            if range_arg is None:
                # The value isn't specified, so we shouldn't diff
                continue

            if not auto_alloc_ranges_equivalent(
                range_arg, ipv6_actual[i].range
            ):
                return True

        return False

    def _create(self, vpc: VPC) -> Optional[VPCSubnet]:
        params = filter_null_values(
            {k: v for k, v in self.module.params.items() if k in CREATE_FIELDS}
        )

        try:
            return vpc.subnet_create(**params)
        except Exception as exception:
            return self.fail(msg="failed to create VPC: {0}".format(exception))

    def _update(self, subnet: VPCSubnet) -> None:
        # VPC Subnets cannot be updated
        handle_updates(
            subnet,
            self.module.params,
            set(),
            self.register_action,
            ignore_keys={"ipv6"},
        )

        if subnet.ipv6 is not None and self.__ipv6_updated(subnet):
            self.fail(msg="IPv6 cannot be updated after VPC subnet creation.")

    def _handle_present(self) -> None:
        params = self.module.params

        vpc = self._get_resource_by_id(VPC, self.module.params.get("vpc_id"))

        subnet = safe_find(
            lambda: [v for v in vpc.subnets if v.label == params.get("label")]
        )
        if subnet is None:
            subnet = self._create(vpc)
            self.register_action("Created VPC Subnet {0}".format(subnet.id))

        self._update(subnet)

        # Force lazy-loading
        subnet._api_get()

        self.results["subnet"] = subnet._raw_json

    def _handle_absent(self) -> None:
        params = self.module.params
        label = params.get("label")

        vpc = self._get_resource_by_id(VPC, self.module.params.get("vpc_id"))

        subnet = safe_find(
            lambda: [v for v in vpc.subnets if v.label == params.get("label")]
        )
        if subnet is not None:
            self.results["subnet"] = subnet._raw_json

            # If any entities attached to this subnet are in a transient state
            # expected to eventually allow deletions,
            # retry the delete until it succeeds.
            if should_retry_subnet_delete_400s(self.client, subnet):
                retry_on_response_status(self._timeout_ctx, subnet.delete, 400)
            else:
                subnet.delete()

            self.register_action(f"Deleted VPC Subnet {label}")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
        else:
            self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode VPC module"""
    Module()


if __name__ == "__main__":
    main()
