#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode NodeBalancers."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    create_filter_and,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import NodeBalancer, NodeBalancerConfig, NodeBalancerNode

linode_nodebalancer_info_spec = {
    # We need to overwrite attributes to exclude them as requirements
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.integer,
        required=False,
        conflicts_with=["label"],
        description=[
            "The ID of this NodeBalancer.",
            "Optional if `label` is defined.",
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=False,
        conflicts_with=["id"],
        description=[
            "The label of this NodeBalancer.",
            "Optional if `id` is defined.",
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode NodeBalancer."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_nodebalancer_info_spec,
    examples=docs.specdoc_examples,
    return_values={
        "node_balancer": SpecReturnValue(
            description="The NodeBalancer in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/nodebalancers/#nodebalancer-view__responses",
            type="dict",
            sample=docs_parent.result_node_balancer_samples,
        ),
        "configs": SpecReturnValue(
            description="A list of configs applied to the NodeBalancer.",
            docs_url="https://www.linode.com/docs/api/nodebalancers/#config-view__responses",
            type=FieldType.list,
            sample=docs_parent.result_configs_samples,
        ),
        "nodes": SpecReturnValue(
            description="A list of configs applied to the NodeBalancer.",
            docs_url="https://www.linode.com/docs/api/nodebalancers/#node-view",
            type=FieldType.list,
            sample=docs_parent.result_nodes_samples,
        ),
    },
)

linode_nodebalancer_valid_filters = ["id", "label"]


class LinodeNodeBalancerInfo(LinodeModuleBase):
    """Module for getting info about a Linode NodeBalancer"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results: dict = {"node_balancer": None, "configs": [], "nodes": []}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_matching_nodebalancer(self) -> Optional[NodeBalancer]:
        filter_items = {
            k: v
            for k, v in self.module.params.items()
            if k in linode_nodebalancer_valid_filters and v is not None
        }

        filter_statement = create_filter_and(NodeBalancer, filter_items)

        try:
            # Special case because ID is not filterable
            if "id" in filter_items.keys():
                result = NodeBalancer(self.client, self.module.params.get("id"))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.nodebalancers(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get nodebalancer {0}".format(exception)
            )

    def _get_node_by_label(
        self, config: NodeBalancerConfig, label: str
    ) -> Optional[NodeBalancerNode]:
        try:
            return config.nodes(NodeBalancerNode.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get nodebalancer node {0}, {1}".format(
                    label, exception
                )
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for NodeBalancer Info module"""

        node_balancer = self._get_matching_nodebalancer()

        if node_balancer is None:
            return self.fail("failed to get nodebalancer")

        self.results["node_balancer"] = node_balancer._raw_json

        for config in node_balancer.configs:
            self.results["configs"].append(config._raw_json)

            for node in config.nodes:
                node._api_get()

                self.results["nodes"].append(node._raw_json)

        return self.results


def main() -> None:
    """Constructs and calls the Linode NodeBalancer Info module"""
    LinodeNodeBalancerInfo()


if __name__ == "__main__":
    main()
