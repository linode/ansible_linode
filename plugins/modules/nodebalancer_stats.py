#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to view Nodebalancer Stats."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.nodebalancer_statistics as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)

import pdb
import pkgutil

traffic_spec = {
    "in": SpecField(
        type=FieldType.list,
        element_type=FieldType.integer,
        required=True,
        description=[
            "An array of key/value pairs representing unix timestamp and reading for inbound traffic."
        ],
    ),
    "out": SpecField(
        type=FieldType.list,
        element_type=FieldType.integer,
        required=True,
        description=[
            "An array of key/value pairs representing unix timestamp and reading for outbound traffic."
        ],
    ),
}

linode_nodebalancer_stats_spec = dict(
    connections=SpecField(
        type=FieldType.list,
        element_type=FieldType.integer,
        required=True,
        description=[
            "An array of key/value pairs representing unix timestamp and reading for connections to this NodeBalancer."
        ],
    ),
    traffic=SpecField(
        type=FieldType.dict,
        suboptions=traffic_spec,
        required=True,
        description=["Traffic statistics for this NodeBalancer."],
    ),
    title=SpecField(
        type=FieldType.string,
        required=True,
        description=[
            "The title for the statistics generated in this response."
        ],
    ),
)

SPECDOC_META = SpecDocMeta(
    description=["View a Linode NodeBalancers Stats."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_nodebalancer_stats_spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        node_balancer_stats=SpecReturnValue(
            description="The NodeBalancer Stats in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/nodebalancers/#nodebalancer-statistics-view__responses",
            type=FieldType.dict,
            sample=docs.result_node_balancer_stats_samples,
        ),
    ),
)


class Module(LinodeModuleBase):
    """Module for getting info about a NodeBalancer's Statistics"""

    def __init__(self) -> None:
        pdb.set_trace()

        self.required_one_of: List[str] = []
        self.results = dict(
            node_balancer_stats=None,
        )

        self.module_arg_spec = SPECDOC_META.ansible_spec

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for NodeBalancer Statistics module"""

        self.results["account"] = self.client.account()._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the nodebalancer_stats module"""
    Module()


if __name__ == "__main__":
    main()
