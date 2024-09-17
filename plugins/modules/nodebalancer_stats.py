#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to view Nodebalancer Stats."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_stats as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import NodeBalancer

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="node_balancer_stats",
        field_type=FieldType.dict,
        display_name="Node Balancer Stats",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-stats",
        samples=docs.result_nodebalancer_stats_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                NodeBalancer,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.nodebalancers,
                NodeBalancer.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
    ],
    examples=docs.specdoc_examples,
)

SPECDOC_META = module.spec

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

if __name__ == "__main__":
    module.run()
