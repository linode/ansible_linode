#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode VPCs."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc as docs
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
    safe_find,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_networking import (
    auto_alloc_ranges_equivalent,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import VPC

SPEC = {
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
    "description": SpecField(
        type=FieldType.string,
        default=None,
        description=["A description describing this VPC."],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The region this VPC is located in."],
    ),
    "ipv6": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        description=[
            "A list of IPv6 ranges in CIDR notation.",
            "NOTE: IPv6 VPCs may not currently be available to all users.",
        ],
        suboptions={
            "range": SpecField(
                type=FieldType.string,
                description="The IPv6 range assigned to this VPC.",
            ),
            "allocation_class": SpecField(
                type=FieldType.string,
                description="The labeled IPv6 Inventory that the VPC Prefix "
                + "should be allocated from.",
            ),
        },
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Create, read, and update a Linode VPC.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "vpc": SpecReturnValue(
            description="The VPC in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpc",
            type=FieldType.dict,
            sample=docs.result_vpc_samples,
        )
    },
)

CREATE_FIELDS = {"label", "region", "description", "ipv6"}
MUTABLE_FIELDS = {"description"}

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
            required_if=[("state", "present", ["region"])],
        )

    def __ipv6_updated(self, vpc: VPC) -> bool:
        ipv6_arg = self.module.params.get("ipv6")
        ipv6_actual = vpc.ipv6

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

    def _create(self) -> Optional[VPC]:
        params = filter_null_values(
            {k: v for k, v in self.module.params.items() if k in CREATE_FIELDS}
        )

        try:
            return self.client.vpcs.create(**params)
        except Exception as exception:
            return self.fail(msg="failed to create VPC: {0}".format(exception))

    def _update(self, vpc: VPC) -> None:
        handle_updates(
            vpc,
            self.module.params,
            MUTABLE_FIELDS,
            self.register_action,
            ignore_keys={"ipv6"},
        )

        if vpc.ipv6 is not None and self.__ipv6_updated(vpc):
            self.fail(msg="IPv6 cannot be updated after VPC creation.")

    def _handle_present(self) -> None:
        params = self.module.params

        vpc = safe_find(self.client.vpcs, VPC.label == params.get("label"))
        if vpc is None:
            vpc = self._create()
            self.register_action("Created VPC {0}".format(vpc.id))

        self._update(vpc)

        # Force lazy-loading
        vpc._api_get()

        self.results["vpc"] = vpc._raw_json

    def _handle_absent(self) -> None:
        params = self.module.params
        label = params.get("label")

        vpc = safe_find(self.client.vpcs, VPC.label == label)

        if vpc is not None:
            self.results["vpc"] = vpc._raw_json
            vpc.delete()
            self.register_action(f"Deleted VPC {label}")

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
