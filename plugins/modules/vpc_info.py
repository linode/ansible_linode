#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode VPC."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    get_resource_safe,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import VPC

spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.integer,
        description=["The ID of the VPC."],
        conflicts_with=["label"],
    ),
    "label": SpecField(
        type=FieldType.string,
        description=["The label of the VPC."],
        conflicts_with=["id"],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode VPC."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "vpc": SpecReturnValue(
            description="The VPC in JSON serialized form.",
            docs_url="TODO",
            type=FieldType.dict,
            sample=docs_parent.result_vpc_samples,
        )
    },
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode VPC"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"vpc": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
            mutually_exclusive=[("id", "label")],
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token info module"""

        params = filter_null_values(self.module.params)
        vpc = None

        if "id" in params:
            vpc = self._get_resource_by_id(VPC, params.get("id"))
        elif "label" in params:
            label = params.get("label")
            vpc = get_resource_safe(
                lambda: self.client.vpcs(VPC.label == label)
            )

        if vpc is None:
            raise ValueError("Could not find VPC with the provided information")

        self.results["vpc"] = vpc._raw_json

        return self.results


if __name__ == "__main__":
    Module()
