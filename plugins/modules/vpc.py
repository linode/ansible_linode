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
            docs_url="TODO",
            type=FieldType.dict,
            sample=docs.result_vpc_samples,
        )
    },
)

CREATE_FIELDS = {"label", "region", "description"}
MUTABLE_FIELDS = {"description"}


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode VPCS"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"changed": False, "actions": [], "vpc": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_if=[("state", "present", ["region"])],
        )

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
            vpc, self.module.params, MUTABLE_FIELDS, self.register_action
        )

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
