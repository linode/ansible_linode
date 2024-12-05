#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module allows users to allocate a new IPv4 Address on their accounts."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
)
from ansible_specdoc.objects import FieldType, SpecDocMeta, SpecField

spec: dict = {
    "linode_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=[
            "The ID of a Linode you have access to "
            "that this address will be allocated to."
        ],
    ),
    "public": SpecField(
        type=FieldType.bool,
        required=True,
        description=["Whether to create a public or private IPv4 address."],
    ),
    "type": SpecField(
        type=FieldType.string,
        required=True,
        choices=["ipv4"],
        description=[
            "The type of address you are requesting. "
            "Only IPv4 addresses may be allocated through this operation."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Allocates a new IPv4 Address on your Account. "
        "The Linode must be configured to support "
        "additional addresses - "
        "please Open a support ticket "
        "requesting additional addresses before attempting allocation.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={},
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for allocating a new IP"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "ip": None,
        }
        super().__init__(module_arg_spec=self.module_arg_spec)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for ip module"""
        params = filter_null_values(self.module.params)
        linode_id = params.get("linode_id")
        public = params.get("public")

        try:
            ip = self.client.networking.ip_allocate(linode_id, public)
            self.register_action(
                f"IP allocation to Linode {linode_id} completed."
            )
        except Exception as exc:
            self.fail(msg=f"failed to allocate IP to Linode {linode_id}: {exc}")

        self.results["ip"] = ip._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
