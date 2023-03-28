#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to view Nodebalancer Stats."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_stats as docs,
)
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

linode_nodebalancer_stats_spec = dict(
    state=SpecField(type=FieldType.string, required=False, doc_hide=True),
    id=SpecField(
        type=FieldType.integer,
        description=[
            "The id of the nodebalancer for which the statistics apply to."
        ],
    ),
    label=SpecField(
        type=FieldType.string,
        description=[
            "The label of the nodebalancer for which the statistics apply to."
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
            docs_url="https://www.linode.com/docs/api/nodebalancers/"
            + "#nodebalancer-statistics-view__responses",
            type=FieldType.dict,
            sample=docs.result_nodebalancer_stats_samples,
        ),
    ),
)


class Module(LinodeModuleBase):
    """Module for getting info about a NodeBalancer's Statistics"""

    def __init__(self) -> None:
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

        self.results["node_balancer_stats"] = self.client.get(
            "/nodebalancers/{}/stats".format(kwargs["id"])
        )

        return self.results


def main() -> None:
    """Constructs and calls the nodebalancer_stats module"""
    Module()


if __name__ == "__main__":
    main()
