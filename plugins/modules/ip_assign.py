#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module allows users to assign IP addresses to multiple Linodes in one Region."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_assign as docs
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
from linode_api4 import Instance
from linode_api4.objects.base import MappedObject

linode_ip_assignments_spec: dict = {
    "address": SpecField(
        type=FieldType.string,
        required=True,
        description=["The IPv4 address or IPv6 range."],
    ),
    "linode_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=["ID of the Linode."],
    ),
}

spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "assignments": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_ip_assignments_spec,
        required=True,
        editable=True,
        description=["List of assignments to make."],
    ),
    "region": SpecField(
        type=FieldType.string,
        required=True,
        description=["The Region to operate in."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Assign IPs to Linodes in a given Region.",
        "The following restrictions apply:",
        " - All Linodes involved must have at least"
        " one public IPv4 address after assignment.",
        " - Linodes may have no more than one assigned private IPv4 address.",
        " - Linodes may have no more than one assigned IPv6 range.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={},
)


class Module(LinodeModuleBase):
    """Module for assigning IPs to Linodes in a given Region"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
        }
        super().__init__(module_arg_spec=self.module_arg_spec)

    def flatten_ips(self, ips: MappedObject) -> list:
        """Flatten a linodes IPs to quickly check the assignment"""
        addrs = [
            v.address
            for v in ips.ipv4.public + ips.ipv4.private + ips.ipv4.reserved
        ]
        addrs += [v.range for v in ips.ipv6.ranges]
        return addrs

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for ip_assign module"""
        params = filter_null_values(self.module.params)
        assignments = params.get("assignments")
        region = params.get("region")

        try:
            for assignment in assignments:
                linode = Instance(self.client, assignment["linode_id"])
                if assignment["address"] in self.flatten_ips(linode.ips):
                    return self.results
            self.client.networking.ips_assign(region, *assignments)
            self.register_action(f"IP assignments completed: {assignments}")
        except Exception as exc:
            self.fail(msg=f"failed to set IP assignments {assignments}: {exc}")

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
