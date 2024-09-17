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
    safe_find,
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

CREATE_FIELDS = {"label", "ipv4"}

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
        handle_updates(subnet, self.module.params, set(), self.register_action)

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
