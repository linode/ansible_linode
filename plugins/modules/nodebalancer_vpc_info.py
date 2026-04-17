#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a
Linode NodeBalancer VPC configuration."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_vpc_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleParam,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import NodeBalancer

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="vpc_config",
        field_type=FieldType.dict,
        display_name="VPC Configuration",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-vpc-config",
        samples=docs_parent.result_vpc_samples,
    ),
    params=[
        InfoModuleParam(
            display_name="VPC Config",
            name="vpc_config_id",
            type=FieldType.integer,
        )
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            description="The ID of the NodeBalancer to retrieve the VPC configuration from.",
            get=lambda client, params: NodeBalancer(client, params.get("id"))
            .vpc(params["vpc_config_id"])
            ._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            description="The label of the NodeBalancer to retrieve the VPC configuration from.",
            get=lambda client, params: safe_find(
                client.nodebalancers,
                NodeBalancer.label == params.get("label"),
                raise_not_found=True,
            )
            .vpc(params["vpc_config_id"])
            ._raw_json,
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
