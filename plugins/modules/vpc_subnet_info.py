#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode VPC Subnet."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    get_resource_safe_condition,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import VPC, VPCSubnet

spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "vpc_id": SpecField(
        type=FieldType.integer,
        description=["The ID of the VPC."],
        required=True,
    ),
    "label": SpecField(
        type=FieldType.string,
        description=["The label of the VPC."],
        conflicts_with=["id"],
    ),
    "id": SpecField(
        type=FieldType.integer,
        description=["The ID of the VPC."],
        conflicts_with=["label"],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode VPC Subnet."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "subnet": SpecReturnValue(
            description="The VPC Subnet in JSON serialized form.",
            docs_url="TODO",
            type=FieldType.dict,
            sample=docs_parent.result_subnet_samples,
        )
    },
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode VPC"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"subnet": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
            mutually_exclusive=[("id", "label")],
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token info module"""

        params = filter_null_values(self.module.params)
        subnet = None

        if "id" in params:
            subnet = self._get_resource_by_id(
                VPCSubnet, params.get("id"), parent_id=params.get("vpc_id")
            )
        elif "label" in params:
            subnet = get_resource_safe_condition(
                lambda: VPC(self.client, params.get("vpc_id")).subnets,
                lambda v: v.label == params.get("label"),
            )

        if subnet is None:
            raise ValueError(
                "Could not find VPC Subnet with the provided information"
            )

        self.results["subnet"] = subnet._raw_json

        return self.results


if __name__ == "__main__":
    Module()
